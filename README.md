# murmur
Murmur utilizes an array of Raspberry Pi modules, with each module connected to 3 microphones, in order to detect open seating in a library space by running a custom sound detection algorithm.

## Usage
#### On server: 
1. Run `app.py`
2. Open the hosted website

#### On each Raspberry Pi:
1. Run `setup.sh` to install required dependencies (assuming using Raspian).
2. Configure `config.py` by updating the `UPLOAD_URL` to the API endpoint of the server and `MIC_RATE` and `DEV_INDEXES` to match the current audio IO devices connected to the Raspberry Pi.
 + To run in development, consider using a service like ngrok
 + Consider updating `MODULE_ID`, `RECORD_TIME` and `OUTPUT_FILENAME`. 
3. Run `app.py`
