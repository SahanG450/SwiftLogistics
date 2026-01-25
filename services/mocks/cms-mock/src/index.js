// SwiftLogistics CMS Mock
// SOAP Server Simulator

const express = require('express');
const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.text({ type: 'text/xml' }));

app.get('/cms', (req, res) => {
  const wsdl = `<?xml version="1.0" encoding="UTF-8"?>
<definitions name="CMSService"
   targetNamespace="http://swiftlogistics.com/cms"
   xmlns="http://schemas.xmlsoap.org/wsdl/"
   xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
   xmlns:tns="http://swiftlogistics.com/cms"
   xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <message name="ProcessOrderRequest">
    <part name="orderId" type="xsd:string"/>
  </message>
  <message name="ProcessOrderResponse">
    <part name="status" type="xsd:string"/>
  </message>
</definitions>`;
  res.set('Content-Type', 'text/xml');
  res.send(wsdl);
});

app.post('/cms', (req, res) => {
  console.log('📨 CMS Mock received SOAP request');
  const response = `<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ProcessOrderResponse>
      <status>SUCCESS</status>
    </ProcessOrderResponse>
  </soap:Body>
</soap:Envelope>`;
  res.set('Content-Type', 'text/xml');
  res.send(response);
});

app.listen(PORT, () => {
  console.log(`✅ CMS Mock (SOAP) listening on port ${PORT}`);
});
