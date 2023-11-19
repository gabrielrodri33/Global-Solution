import requests
import json

def consultaCpf(cpf):
  url = "https://api.gw.cellereit.com.br/bg-check/cpf-simples"
  payload = json.dumps({"cpf": cpf,
    "databases": [
      "basic_data"
    ]})

  token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzS1dxVWt4U2pTSDc5OUxnc3cyX0htRFozZDlkVzZoNmtsVGx2Q2t2dkdzIn0.eyJleHAiOjE2OTgyOTAwMTYsImlhdCI6MTY5ODI4OTcxNiwianRpIjoiODQ3MDc1MzItNjExNS00YjY4LWFiOGItNTA4NzE2Nzk0NWY0IiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5jZWxsZXJlaXQuY29tLmJyL2F1dGgvcmVhbG1zL3BvcnRhbC1jbGllbnRlcy1hcGkiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNDRlMjU5NWUtOGQwZS00OTE3LTkxMzEtYmE0MmRjNWIwMTgyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoicGRjYS1hcGkiLCJzZXNzaW9uX3N0YXRlIjoiMzU5MWUyZTEtODAxMi00NzQzLTg0MWUtOTJkYjQwOTg5ZjYxIiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtcG9ydGFsLWNsaWVudGVzLWFwaSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJlbWFpbCBwbGFucyBwcm9maWxlIiwic2lkIjoiMzU5MWUyZTEtODAxMi00NzQzLTg0MWUtOTJkYjQwOTg5ZjYxIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImdyb3VwcyI6WyJhY2NvdW50QWRtaW5zIiwiaW5kaXZpZHVhbHMiXSwiYmlsbGluZ0FjY291bnRJZCI6IjY1MzlkODM0NWFjMGVjMTkxY2IxNzI2YSIsInByZWZlcnJlZF91c2VybmFtZSI6ImdhYnJpZWxyb2RyaTMzM0BnbWFpbC5jb20iLCJnaXZlbl9uYW1lIjoiIiwibG9jYWxlIjoicHQtQlIiLCJmYW1pbHlfbmFtZSI6IiIsImVtYWlsIjoiZ2FicmllbHJvZHJpMzMzQGdtYWlsLmNvbSJ9.dfkSMEsaPmE9M2L5sCjukZo7VcCfNHHcRUT5hsMHITHKFlcxaQIVRhhoIOQBvbzvueYToYZtzVSWiRW8_4WHvfyBeATrNBTEn4WT2XzEEXeS26lBWej-xKCio_ggb5A90eBx1ooHqm36yr0tAoTjvY2hgyC8J4y2xGTENeEzBZgLY-uBzJfWYp5PI3xMc9JwrlgZtwI0LxMitY7TOP6-ZA3m3VsBt9Ypv3bOJ5pA9tLtLaZD_q-TWlbNeAZ06ibhgUFsViITx36IQYPMfUKR6Bf74BNdtjEY3v-jyGyqqzcHayvUqoJN4lo04liHWzUHbY-4FHbt6ZE8D8aR7Tdwlg"

  headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

  response = requests.request("POST", url, headers=headers, data=payload)

  if response.status_code == 200:
    data = response.json()

    tax_id_status = data[0]['BasicData']['TaxIdStatus']

    is_regular = tax_id_status == "REGULAR"

    return True

  else:
    return False