#include <RFM69.h>

#define MICROPRO_CSPIN 10
#define MICROPRO_IPIN  3
#define IS_RFM69HW     true
#define FREQUENCY      RF69_915MHZ
#define ACK_CHAR       '\n'
#define NACK_CHAR      '\r'

typedef enum
{
  none,
  test,
  configure,
  write_packet,
  read_packet,
  invalid
} COMMAND;

RFM69 radio(MICROPRO_CSPIN, MICROPRO_IPIN, IS_RFM69HW);

void setup()
{
  Serial.begin(9600);
  while(!Serial);
}

void loop()
{
  static char cmd[64];
  static int cmd_len = 0;
  static COMMAND cmd_type = none;
  static bool read_valid = false;
  uint16_t sender_id;
  uint16_t rssi;
  int datalen;
  char output[RF69_MAX_DATA_LEN];
  
  if(radio.receiveDone())
  {
    read_valid = true;
    sender_id = radio.SENDERID;
    rssi = radio.RSSI;
    datalen = (int) radio.DATALEN;
    for(int i=0; i<datalen; ++i)
      output[i] = radio.DATA[i];
  }
  if(Serial.available())
  {
    cmd[cmd_len] = Serial.read();
    cmd_len += 1;
    if(cmd[cmd_len-1] == ACK_CHAR)
    {
      if(cmd[0] == 't')
        cmd_type = test;
      else if(cmd[0] == 'c')
        cmd_type = configure;
      else if(cmd[0] == 'w')
        cmd_type = write_packet;
      else if(cmd[0] == 'r')
        cmd_type = read_packet;
      else
        cmd_type = invalid;
    }
  }
  if(cmd_type == test) // transmit ACK to demonstrate that arduino is active
  {
    Serial.print(ACK_CHAR);
    cmd_type = none;
    cmd_len = 0;
  }
  else if(cmd_type == configure) // configure radio network and node ID
  {
    uint8_t network_id = (uint8_t) cmd[1];
    uint16_t self_id = (((uint16_t) cmd[2]) >> 8) | (((uint16_t) cmd[3]) & 0xFF);
    radio.initialize(FREQUENCY, self_id, network_id);
    Serial.print(ACK_CHAR);
    cmd_type = none;
    cmd_len = 0;
  }
  else if(cmd_type == write_packet) // transmit a packet
  {
    uint16_t target_id = (((uint16_t) cmd[1]) >> 8) | (((uint16_t) cmd[2]) & 0xFF);
    radio.send(target_id, cmd+3, cmd_len-4);
    Serial.print(ACK_CHAR);
    cmd_type = none;
    cmd_len = 0;
  }
  else if(cmd_type == read_packet) // read a packet, or NACK if none is available
  {
    if(!read_valid) // No packet is available
      Serial.print(NACK_CHAR);
    else // Output sender ID, RSSI, and contents of packet
    {
      Serial.print(ACK_CHAR);
      Serial.print((char) (sender_id >> 8));
      Serial.print((char) (sender_id & 0xFF));
      Serial.print((char) (rssi >> 8));
      Serial.print((char) (rssi & 0xFF));
      for(int i=0; i<datalen; i++)
        Serial.print((char) output[i]);
      Serial.print(ACK_CHAR);
      read_valid = false;
    }
    cmd_type = none;
    cmd_len = 0;
  }
  else if(cmd_type == invalid) // NACK improperly-formatted command
  {
    Serial.print(NACK_CHAR);
    cmd_type = none;
    cmd_len = 0;
  }
}
