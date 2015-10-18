require 'rubygems'
require 'savon'
require 'pp'

url = "http://ws.nasdaqdod.com/v1/NASDAQAnalytics.asmx?WSDL"


soap_header = {
    "Header" => {
         "@xmlns" => "http://www.xignite.com/services/",
         "Username" => "mit-hacker0@nasdaq.com"
         }
    }

client = Savon.client(wsdl: url, :soap_header => soap_header, convert_request_keys_to: :none, env_namespace: 'soap')

response = client.call(:get_vwap, message: {
    "@xmlns" => "http://www.xignite.com/services/",
        Symbols: 'NDAQ, GOOG',
        StartDateTime: '9/18/2015 09:30:00.000',
        EndDateTime: '9/18/2015 10:30:00.000',
        MarketCenters: 'Q, B',
        SalesConditions: '@, T'
})


pp response.to_hash
