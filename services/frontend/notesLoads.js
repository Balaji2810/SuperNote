if(getCookie('token') === null) window.location.href='/login.html'
autoPopulateInput();

// Function to auto-populate the input field
function autoPopulateInput() {
    var inputElement = document.getElementById('autocomplete-input');
    var datalist = document.getElementById('suggestions');

    apiRequest('GET', "/api/users")
    .then(data => {
       
        if(data.message==="Success")
        {
           
        
            for (const item of data.data) {
                addUser(item.username,item.id);
                
            }
           
            
        }
        
    })
    .catch(error => {
        console.error('GET error:', error);
    });
}

// Function to get the selected value
function getSelectedValue() {
    var inputElement = document.getElementById('autocomplete-input');
    var datalist = document.getElementById('suggestions');
    
    var options = datalist.getElementsByTagName('option');
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
      });
      let room_id = params.note; // "some_value"
      let type = params.type;

    for (var i = 0; i < options.length; i++) {
        if (options[i].value === inputElement.value) {
            // You can do something with the selected value here
            console.log('Selected Value: ' + options[i].value);
            postData={"user_id":options[i].id,"note_id":room_id}
            console.log(postData);
            apiRequest('POST', "/api/notes/share", postData)
                .then(data => {
                    console.log('POST:', data);
                                       
                })
                .catch(error => {
                    console.error('POST error:', error);
                    alert("Already shared with this user"); 
                });
                document.getElementById("autocomplete-input").value = "";
            break;
        }
    }
}

function openPopup() {
    var popup = document.getElementById("namePopup");
    popup.style.display = "block";
}

function closePopup() {
    var popup = document.getElementById("namePopup");
    popup.style.display = "none";
}

function shareName() {
    // var selectedName = document.getElementById('nameInput').value;
    // alert("Shared Name: " + selectedName);
    getSelectedValue()
    closePopup();
}

function addUser(name, userid) {
    var datalist = document.getElementById("suggestions");

    // Create a new option element
    var newOption = document.createElement("option");
    newOption.textContent = name; // Set the text for the new option
    newOption.id = userid;
    

    // Append the new option to the datalist
    datalist.appendChild(newOption);
}