loadMyNotes()
loadSharedNotes()

if(getCookie('token') === null) window.location.href='/login.html'

        const setActiveTab = (tab_name) => {
            Array(...document.getElementsByClassName('tab')).forEach(elem => {
                elem.classList.remove('active');
            })
            event.target.classList.add('active')
            const note_list_a = document.getElementById('notes-list-a');
            const note_list_b = document.getElementById('notes-list-b');

            // note_list_a.style.display = 'none'; 
            note_list_a.style.visibility = 'hidden';

            // note_list_b.style.display = 'none'; 
            note_list_b.style.visibility = 'hidden';
            if(tab_name==="my-notes")
            {
                // note_list_a.style.display = 'block'; 
                note_list_a.style.visibility = 'visible';
            }
            else
            {
                // note_list_b.style.display = 'block'; 
                note_list_b.style.visibility = 'visible';
            }
        }

function logout(){
    apiRequest('DELETE',"/api/logout")
        .then(() => {
          console.log('logged out!!');
          window.location.href="/login.html"
        })
        .catch(error => {
          console.error('logout error:', error);
        });
}    

function showPopup() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
}

// Function to close the popup
function closePopup() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("popup").style.display = "none";
}

// Function to save the note (you can modify this part to handle the note data)
function saveNote() {
    const noteName = document.getElementById("noteName").value;
    if (noteName.trim() === "") {
        alert("Note name required.");
        return
    }
    const postData = { name: noteName.trim()};
    apiRequest('POST', "/api/notes", postData)
    .then(data => {
        console.log('POST:', data);
        if(data.message==="Success")
        {
            createCard(data.data.name, data.data.id, "notes-list-a");
            alert("Note Name: " + noteName +" created!!"); // Replace this with your desired action
        }
        
    })
    .catch(error => {
        console.error('POST error:', error);
        alert(noteName +" not created!!")
    });
    closePopup();
}

function createCard(name,card_id, container_id) {
    const cardContainer = document.getElementById(container_id);
    
    const card = document.createElement("div");
    card.classList.add("card");

    const cardName = document.createElement("h1");
    cardName.innerText = name;

    let type = "";

    if(container_id === "notes-list-b")
    {
        type = "shared"
    }
    else
    {
        type = "mynote"
    }

    card.addEventListener("click", function() {
        window.location.href="/notes.html?note="+card_id+"&type="+type
    });

    card.appendChild(cardName);
    cardContainer.appendChild(card);
}

function loadMyNotes()
{
    apiRequest('GET', "/api/notes")
    .then(data => {
        if(data.message==="Success")
        {
            for (const item of data.data) {
                createCard(item.name, item.id, "notes-list-a");
            }
            
        }
        
    })
    .catch(error => {
        console.error('GET error:', error);
        alert("Cards not loaded!!")
    });
}

function loadSharedNotes()
{ 
    // alert("loadSharedNotes")
    apiRequest('GET', "/api/notes/shared")
    .then(data => {
        if(data.message==="Success")
        {   
            for (const item of data.data) {
                createCard(item.name, item._id, "notes-list-b");
                console.log(item.name, item._id, "notes-list-b");
            }
            
        }
        
    })
    .catch(error => {
        console.error('POST error:', error);
        alert("Cards not loaded!!")
    });
}

