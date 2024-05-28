async function fetchData() {
    try {
      const response = await fetch('/api/data');
      const data = await response.json();
  
      document.getElementById('irValue').textContent = data.ir;
      document.getElementById('redValue').textContent = data.red;
      document.getElementById('ecgValue').textContent = data.ecg;
  
      if (data.lat !== null && data.lon !== null) {
        document.getElementById('location').textContent = `Lat: ${data.lat}, Lon: ${data.lon}`;
      } else {
        document.getElementById('location').textContent = 'Location data not available';
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
  
  setInterval(fetchData, 5000); // Fetch new data every 5 seconds
  fetchData(); // Initial fetch
  