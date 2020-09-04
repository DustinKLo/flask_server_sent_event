var sse = () => {
  var estream = new EventSource("/stream");
  estream.onopen = (e) => console.log(e);
  estream.onmessage = (e) => console.log(e.data);
  estream.onstatus = (e) => console.log(e);
  estream.onerror = (e) => {
    console.error(e);
    console.error("CLOSING SERVER EVENT STREAM");
    estream.close();
  };
};
sse();
