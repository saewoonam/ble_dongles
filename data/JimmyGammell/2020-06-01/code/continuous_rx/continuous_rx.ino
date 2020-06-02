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

typedef struct
{
  bool valid;
  char message[64];
  int  message_len;
  uint16_t sender_id;
  uint16_t rssi;
} packet;

RFM69 radio(MICROPRO_CSPIN, MICROPRO_IPIN, IS_RFM69HW);
packet latest_packet;

void setup() 
{
  Serial.begin(9600);
  radio.initialize(FREQUENCY, RX_ID, NETWORK_ID);
  //radio._isRFM69HW = false;
  //radio.writeReg(0x5A, 0x55);
  //radio.writeReg(0x5C, 0x70);
  //radio.writeReg(0x11, (POWER_LEVEL & 0x1F) | 0x40);
  latest_packet.valid = false;
  while(!Serial);
}

void loop() 
{
  if(radio.receiveDone())
  {
    latest_packet.valid = true;
    latest_packet.message_len = (int) radio.DATALEN;
    for(int i=0; i<latest_packet.message_len; ++i)
      latest_packet.message[i] = (char) radio.DATA[i];
    latest_packet.rssi = radio.RSSI;
    latest_packet.sender_id = radio.SENDERID;
  }
  if(Serial.available())
  {
    if(Serial.read() != '\n');
    else if(latest_packet.valid)
    {
      Serial.print('y');
      Serial.print((char) (latest_packet.sender_id >> 8));
      Serial.print((char) (latest_packet.sender_id & 0xFF));
      Serial.print((char) (latest_packet.rssi >> 8));
      Serial.print((char) (latest_packet.rssi & 0xFF));
      for(int i=0; i<latest_packet.message_len; ++i)
        Serial.print((char) latest_packet.message[i]);
      Serial.print('\n');
      latest_packet.valid = false;
    }
    else
    {
      Serial.print('n');
      Serial.print('\n');
    }
  }
}
