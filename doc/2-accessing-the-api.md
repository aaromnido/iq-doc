# 2. Accessing the API

## 2.1. Basic Usage with cURL

To interact with the **Inspiration-Q Index Tracking API** using `curl`, use the following command:

```sh
curl -X POST https://www.inspiration-q.com/api/v1/iq-finance/index-tracking \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "Ocp-Apim-Subscription-Key: <your-api-key>" \
     -d '{
  "assets_utility_matrix": [
    [3.571705619883564, -0.7955365555749586, 0.12557964034596986, 1.0639482728918976, -0.40191777016183283, 0.6863605725971405, -0.13949908918445247, 0.1711775516765147, 0.6755160399639315, 2.51293081246698],
    [-0.7955365555749586, 5.415520138923123, -2.0174005804761763, 0.030388266205496173, 2.550222403729447, 0.5643289518319003, -1.293304939459475, -0.5751123806041349, 3.594236909963808, 1.8956893890593007],
    [0.12557964034596986, -2.0174005804761763, 6.365322954156529, 2.257879191752247, -3.658046606965999, -0.45033274824515956, -1.0273304859751011, -0.21571777326705427, -0.3865083786928926, -1.533229084930434],
    [1.0639482728918976, 0.030388266205496173, 2.257879191752247, 3.9943121946674895, -1.78048417102389, 0.5687925714650388, -1.1084218725187323, -0.1515180112312195, -2.5176791064421384, 1.088241626988272],
    [-0.40191777016183283, 2.550222403729447, -3.658046606965999, -1.78048417102389, 8.390493238417324, 2.2223130935800453, -1.77173431354756, -1.3492997496155428, 3.448640251236081, 0.0298926428035794],
    [0.6863605725971405, 0.5643289518319003, -0.45033274824515956, 0.5687925714650388, 2.2223130935800453, 4.449214575445028, -2.713857481152314, -0.8300224805092693, -0.727328631285821, -0.3117075238989559],
    [-0.13949908918445247, -1.293304939459475, -1.0273304859751011, -1.1084218725187323, -1.77173431354756, -2.713857481152314, 4.0926798019898545, 2.3976179895459238, 0.27049000177733207, -0.29585690145164956],
    [0.1711775516765147, -0.5751123806041349, -0.21571777326705427, -0.1515180112312195, -1.3492997496155428, -0.8300224805092693, 2.3976179895459238, 3.864597206599372, -0.2604720356119854, -1.9647359528399329],
    [0.6755160399639315, 3.594236909963808, -0.3865083786928926, -2.5176791064421384, 3.448640251236081, -0.727328631285821, 0.27049000177733207, -0.2604720356119854, 9.083901928836333, 1.4490996023473937],
    [2.51293081246698, 1.8956893890593007, -1.533229084930434, 1.088241626988272, 0.0298926428035794, -0.3117075238989559, -0.29585690145164956, -1.9647359528399329, 1.4490996023473937, 5.4073509688190695]
  ],
  "assets_to_benchmark_utility_vector": [0.05177358659202069, -0.3356720686060817, 0.3206831344776768, 0.41750733093212566, 0.3313631827597856, -0.13542997653680122, -0.43400507867532734, 0.29062468284108733, 0.15880933369691574, -0.441086589088471],
  "portfolio_size": "8",
  "asset_names": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
  "randomNumberGenerator": "359133650"
}'
```

You will obtain a response like:
```sh
{"computationId":"4cfa2fc9-85c5-429f-bc9f-a29b1e907763","status":"Computing","computationStoreTimeUtc":"2025-03-04T16:18:03.3491589Z"}
```

Then you can launch a `curl` to obtain the result:
```sh
curl -X GET "https://www.inspiration-q.com/api/v1/iq-finance/index-tracking/{indexTrackingComputationId}" \
  -H "Ocp-Apim-Subscription-Key: YOUR_API_KEY"
```

Where you have to substitute `YOUR_API_KEY` with your actual API key, and `{indexTrackingComputationId}` with the `computationId` that you have obtained, `4cfa2fc9-85c5-429f-bc9f-a29b1e907763` in the example.

If the Index Tracking computation have been computed, you will obtain:
```sh
{"computationId":"4cfa2fc9-85c5-429f-bc9f-a29b1e907763","status":"Ok","computationTimeInSeconds":2.24452945962548,"computationStartTimeUtc":"2025-03-04T16:18:07","computationEndTimeUtc":"2025-03-04T16:18:10","computationStoreTimeUtc":"2025-03-04T16:18:03.35","named_solution":{"a":0.0,"b":0.0,"c":0.2173376035533007,"d":0.13579958870253325,"e":0.24133281639039988,"f":0.0,"g":0.0,"h":0.2981627679516593,"i":0.0,"j":0.10736713477033608},"info":0}
```

If it is still running the calculus, you will get:
```sh
{"computationId": "a3984c72-3ae9-4bdf-adee-005b65c1bc9e","status": "Computing","computationStoreTimeUtc": "2025-03-04T12:34:56.8317536Z"}
```


## 2.2. A Postman Collection

### Overview

In the `api` folder, we provide a **Postman collection** named **`Inspiration-Q_Index_Tracking_API.postman_collection.json`**. This collection simplifies API testing and interaction.

### How to Use the Postman Collection

#### 1. Install Postman
- [Download Postman](https://www.postman.com/downloads/)

#### 2. Import the Collection
1. Open **Postman**.
2. Click **File** → **Import**.
3. Select **Upload Files** and choose `api/Inspiration-Q_Index_Tracking_API.postman_collection.json`.
4. Click **Open** to import.

#### 3. Configure Environment Variables
1. Click **Environments** in Postman.
2. Create a new environment `Inspiration-Q API`.
3. Add:
   - **baseUrl**: `https://www.inspiration-q.com/api/v1`
   - **apiKey**: `<your-API-key>`
4. Save the environment and select it before making requests.

#### 4. Make API Requests
- Expand **`Inspiration-Q Index Tracking API`** collection.
- Choose an endpoint (e.g., **Create a new Index Tracking computation**).
- Click **Send** to execute the request.

## 2.3. Using Python Without the SDK

### Prerequisites
- **Python 3** installed.
- **Requests library** (`pip install requests`).
- **API key** for Inspiration-Q.

### Python Script
The script is available in [index_tracking_no_sdk.py](../examples/index_tracking_no_sdk.py) inside the [Examples Folder](../examples/).

```python
import requests
import time

# API Configuration
BASE_URL = "https://www.inspiration-q.com/api/v1"
API_KEY = "YOUR_API_KEY"
HEADERS = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": API_KEY
}

# Payload with provided values
payload = {
    "assets_utility_matrix": [
        [3.5717, -0.7955, 0.1256, 1.0639, -0.4019, 0.6864, -0.1395, 0.1712, 0.6755, 2.5129],
        [-0.7955, 5.4155, -2.0174, 0.0304, 2.5502, 0.5643, -1.2933, -0.5751, 3.5942, 1.8957],
        [0.1256, -2.0174, 6.3653, 2.2579, -3.6580, -0.4503, -1.0273, -0.2157, -0.3865, -1.5332],
        [1.0639, 0.0304, 2.2579, 3.9943, -1.7805, 0.5688, -1.1084, -0.1515, -2.5177, 1.0882],
        [-0.4019, 2.5502, -3.6580, -1.7805, 8.3905, 2.2223, -1.7717, -1.3493, 3.4486, 0.0299],
        [0.6864, 0.5643, -0.4503, 0.5688, 2.2223, 4.4492, -2.7139, -0.8300, -0.7273, -0.3117],
        [-0.1395, -1.2933, -1.0273, -1.1084, -1.7717, -2.7139, 4.0927, 2.3976, 0.2705, -0.2959],
        [0.1712, -0.5751, -0.2157, -0.1515, -1.3493, -0.8300, 2.3976, 3.8646, -0.2605, -1.9647],
        [0.6755, 3.5942, -0.3865, -2.5177, 3.4486, -0.7273, 0.2705, -0.2605, 9.0839, 1.4491],
        [2.5129, 1.8957, -1.5332, 1.0882, 0.0299, -0.3117, -0.2959, -1.9647, 1.4491, 5.4074]
    ],
    "assets_to_benchmark_utility_vector": [0.0518, -0.3357, 0.3207, 0.4175, 0.3314, -0.1354, -0.4340, 0.2906, 0.1588, -0.4411],
    "portfolio_size": 8,
    "asset_names": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    "random_number_generator_seed": 359133650,
    "description": "Index Tracking from a python example, no SDK used"
}

# Step 1: Create a new Index Tracking computation
response = requests.post(f"{BASE_URL}/iq-finance/index-tracking", json=payload, headers=HEADERS)

if response.status_code == 201:
    computation_result = response.json()
    computation_id = computation_result["computationId"]
    print(f"Computation created successfully. ID: {computation_id}")
else:
    print(f"Error creating computation: {response.status_code} - {response.text}")
    exit()

# Step 2: Retrieve the computation results by ID
print("Fetching computation results...")

while True:
    response = requests.get(f"{BASE_URL}/iq-finance/index-tracking/{computation_id}", headers=HEADERS)

    if response.status_code == 200:
        result = response.json()
        print(f"Computation Status: {result['status']}")
        
        if result["status"] in ["Failed", "Ok"]:
            print("Computation complete!")
            print("Computation Details:", result)
            break
    elif response.status_code == 404:
        print("Computation not found. Retrying...")
    else:
        print(f"Error fetching computation: {response.status_code} - {response.text}")
        break

    time.sleep(5)  # Wait before retrying

```

### Notes
- Replace `YOUR_API_KEY` with your actual API key.
- Adjust payload parameters as needed.
- Increase `time.sleep(5)` if needed for longer computations.