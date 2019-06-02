## PubGate Steemit -> ActivityPub bridge
Extension for [PubGate](https://github.com/autogestion/pubgate), federates posts from Steemit blogs 

Requires PubGate >= 0.2.10
### Run
 - Install PubGate
 - Install pg_steemit
 ```
 pip install git+https://github.com/autogestion/pubgate-steemit.git

```
 - Update conf.cfg with
```
EXTENSIONS = [..., "pg_steemit"]

STEEMIT_BOT_TIMEOUT = 3600
FETCH_ON_START = 10
```
 - run
```
python run_api.py

```


### Usage

#### Create bot
```
/user  POST
```
payload
```
{
	"username": "user",
	"password": "pass",
	"email": "admin@mail.com",                                          #optional
	"invite": "xyz",                                                    #required if register by invite enabled
	"profile": {
		"type": "Service",
		"name": "LiberLandPress",
		"summary": "Broadcast from <a href='https://steemit.com/@liberlandpress' target='_blank'>Steemit blog</a>",
	    "icon": {
	        "type": "Image",
	        "mediaType": "image/png",
	        "url": "https://liberland.org/en/assets/images/logo.png"
	    }
	},
	"details": {
		"stbot": {
			"blogs": ["liberlandpress"],
			"enable": true,
			"tags": ["liberland", "steemit", "selfgoverned"]            #could be empty []
		}
	}
}
```


#### Disable/Update bot
```
/<username>  PATCH   (auth required)
```
payload
```
{
    "details": {
        "stbot": {
            "blogs": ["liberlandpress"],                                #change to update channel's list
            "enable": false,                                            #"enable": true to re-enable
			"tags": ["liberland", "steemit", "selfgoverned"]            #could be empty []
        }
    }
}
```
