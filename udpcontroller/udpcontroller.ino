
/*
   stand-alone udp server for controlling digital pins
   on ESP8266 based boards

   not well tested yet...

   by Christian Fiedler

*/

#include <uCRC16Lib.h>
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define DEBUG

#ifdef DEBUG
#define FLUSH Serial.flush()
#else
#define FLUSH
#endif


// The baudrate used for serial output
#define BAUDRATE 115200

#define AP_CHANNEL 1
// hidden SSID does appear to not work :(
#define AP_HIDDEN  false

#define UDP_PORT 10000

const char AP_SSID[] = "lbd";
const char AP_PASS[] = "LearningByDoing";


IPAddress local_IP(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
WiFiUDP udp;

#define STATE_SIZE 16
uint8_t state[STATE_SIZE];

uint8_t ALLOW_ACCESS[8] = { 0x3F, 0xF0, 0x01 };

static uint8_t apply_parameters(uint8_t *data) {
  uint8_t i, j, k, err = 0;

  ESP.wdtFeed();
  memcpy(state, data + 24, STATE_SIZE);

  k = 0;
  for (i = 0; i < 8; i++) {
    uint8_t tmp = state[i];
    uint8_t access = ALLOW_ACCESS[i];
    for (j = 0; j < 8; j++) {
      if ((access & 1) != 0) {
        if ((tmp & 1) != 0) {
          pinMode(k, OUTPUT);
        } else {
          pinMode(k, INPUT_PULLUP);
        }
      }
      tmp >>= 1;
      access >>= 1;
      k++;
    }
  }

  ESP.wdtFeed();
  k = 0;
  for (i = 0; i < 8; i++) {
    uint8_t tmp = state[i + 8];
    uint8_t access = ALLOW_ACCESS[i];
    for (j = 0; j < 8; j++) {
      if ((access & 1) != 0) {
        if (((state[i] >> j) & 1) != 0) {
          if (tmp & 1 != 0) {
            digitalWrite(k, HIGH);
          } else {
            digitalWrite(k, LOW);
          }
        } else if ((tmp & 1) != 0) {
          err = 2; // invalid
        }
      }
      tmp >>= 1;
      access >>= 1;
      k++;
    }
  }

  ESP.wdtFeed();
  k = 0;
  for (i = 0; i < 8; i++) {
    uint8_t tmp = 0;
    uint8_t access = ALLOW_ACCESS[i];
    for (j = 0; j < 8; j++) {
      if ((access & 1) != 0) {
        tmp >>= 1;
        if (digitalRead(k)) {
          tmp |= 0x80;
        }
      }
      access >>= 1;
      k++;
    }
    data[i + 8] = tmp;
  }

  return err;
}

static bool check_crc(uint8_t *packet, int size) {
  size -= 2; // last 2 bytes are CRC
  uint16_t receivedCRC = packet[size] | (packet[size + 1] << 8);
  return uCRC16Lib::calculate((char*) packet, size) == receivedCRC;
}


/*
   incoming packets

     4 bytes magic = "LBD!"
     4 bytes packet ID (random number)
     8 bytes reserved
     8 bytes reserved
     8 bytes bitfield of pins to set to output
     8 bytes bitfield of pins to set to high
     2 bytes CRC
   -----------------
    42 bytes total

   response packets
     1 byte error code (0 = OK)
     3 bytes reserved
     4 bytes packet ID (same as in request)
     8 bytes bitfield of input pins that were high
   -----------------
    16 bytes total

*/

#define PACKET_SIZE 42
void loop()
{
  static const char MAGIC[] = "LBD!";
#define MAGIC_LEN 4

  uint8_t packet[MAX_PACKET_SIZE];
  int packsz = udp.parsePacket();
  uint8_t error = 0;


  if (packsz == PACKET_SIZE) {
    int i = udp.read(packet, PACKET_SIZE);
    if (i != PACKET_SIZE) {
      // wat?
      Serial.println("Package and read size don't match");
      return;
    }

    if (memcmp(packet, MAGIC, MAGIC_LEN) != 0) {
      // this packet is not for us
      Serial.println("No magic");
      return;
    }

    if (!check_crc(packet, PACKET_SIZE)) {
      packet[0] = 1; // 1 = wrong CRC
      Serial.println("wrong CRC");
      goto respond;
    }

    Serial.println("Applying...");
    FLUSH;

    packet[0] = apply_parameters(packet);

respond:
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write(packet, 8);
    udp.endPacket();

    Serial.println("Done.");
    FLUSH;
  } else if (packsz != 0) {
    Serial.println("Wrong package size");
    Serial.println(packsz);
  }
}

void setup()
{
  Serial.begin(BAUDRATE);
  Serial.println();
  Serial.println("Starting...");

  int success = WiFi.softAPConfig(local_IP, gateway, subnet);
  if (!success) {
    goto fail;
  }

  success = WiFi.softAP(AP_SSID, AP_PASS, AP_CHANNEL, AP_HIDDEN);
  if (!success) {
    goto fail;
  }


  Serial.printf("SSID: %s\r\nPASS: %s\r\nIP:   ", AP_SSID, AP_PASS);
  Serial.println(WiFi.softAPIP());

  memset(state, 0, STATE_SIZE);
  udp.begin(UDP_PORT);

  Serial.println("Ready.");
  Serial.flush();
  return;

fail:
  Serial.println("Failed to set up AP...");
  delay(5000);

}



