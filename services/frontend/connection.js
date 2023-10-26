
function apiRequest(method, url, data = null) {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json', // You can adjust this based on your API's requirements
      },
    };
  
    if (data) {
      options.body = JSON.stringify(data);
    }
  
    return fetch(url, options)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
  
        if (method === 'DELETE') {
          return null; // No response data for DELETE requests
        }
  
        return response.json(); // Assuming the server responds with JSON data.
      });
  }

  function getCookie(name) {
    // Split the cookies string into individual cookies
    var cookies = document.cookie.split('; ');
  
    // Loop through the cookies and look for the one with the specified name
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var cookieParts = cookie.split('=');
  
      // Check if the name of the cookie matches the desired name
      if (cookieParts[0] === name) {
        // Return the value of the cookie
        return decodeURIComponent(cookieParts[1]);
      }
    }
  
    // If the cookie is not found, return null
    return null;
  }

  