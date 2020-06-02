#include <RFM69.h>

#define MICROPRO_CSPIN 10
#define MICROPRO_IPIN  3
#define IS_RFM69HW     true
#define FREQUENCY      RF69_915MHZ
#define NETWORK_ID     0
#define TX_ID          1
#define RX_ID          2
#define PACKET         "abcde"
#define PACKET_LEN     5
#define POWER_LEVEL    18

RFM69 radio(MICROPRO_CSPIN, MICROPRO_IPIN, IS_RFM69HW);

void setup() 
{
  radio.initialize(FREQUENCY, TX_ID, NETWORK_ID);
  //radio._isRFM69HW = false;
  //radio.writeReg(0x5A, 0x55);
  //radio.writeReg(0x5C, 0x70);
  //radio.writeReg(0x11, (POWER_LEVEL & 0x1F) | 0x40);
}

void loop() {
  delay(100);
  radio.send(RX_ID, PACKET, PACKET_LEN);
}
