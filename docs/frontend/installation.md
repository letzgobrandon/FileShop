# Frontend -> Installation

Follow the instructions below to setup your Frontend Server

## Requirements

Make sure you have [Node](https://nodejs.org/en/download/package-manager/) and [npm](https://www.npmjs.com/) installed. Node 12 is tested and working.

You'll also need to install vue and other dependecies. These can be installed by running the following command inside the frontend folder.

```bash
# Move to frontend repo
cd frontend

# Install dependecies
npm install
```

## Configure

Configure your backend URL in `apiendpoints.js` -> `BASE`, e.g. `http://localhost:8000` or `https://api.fileshop.online` without a trailing slash.

## Running the server

To run the server, run

```bash
npm run serve

# To customise the port
npm run serve -- --port 8080
```
