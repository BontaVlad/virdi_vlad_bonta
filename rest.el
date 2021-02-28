-*- restclient -*-

:base-url = http://127.0.0.1:8000
# Start Date: 2013-03-20 
# Initial Balance: $32500 
# Portfolio Allocation: AAPL: 20% GOOG: 50% VTI: 30% 


POST :base-url/symbols
Content-Type: application/json
{
  "date_from": "2013-03-20",
  "initial_balance": 32500,
  "symbols": [
    {
      "name": "AAPL",
      "allocation": 20
    },
    {
      "name": "GOOG",
      "allocation": 50
    },
    {
      "name": "VTI",
      "allocation": 30
    }
  ]
}
