/* eslint-env browser */

import * as Y from 'yjs'
// import { WebsocketProvider } from 'y-websocket'
import { WebrtcProvider } from 'y-webrtc'
import { QuillBinding } from 'y-quill'
import Quill from 'quill'
import QuillCursors from 'quill-cursors'

// Quill.register('modules/handlers')
Quill.register('modules/cursors', QuillCursors)

window.addEventListener('load', () => {
  const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
  let room_id = params.note; // "some_value"
  const ydoc = new Y.Doc()
  //const provider = new WebsocketProvider('wss://demos.yjs.dev', 'quill-demo-4', ydoc)
  const provider = new WebrtcProvider(room_id, ydoc, { password: 'optional-room-password', signaling:['ws://localhost/websocket/signal'] })
  const yarray = ydoc.get('array', Y.Array)
  const ytext = ydoc.getText('quill')
  const editorContainer = document.createElement('div')
  editorContainer.setAttribute('id', 'editor')
  document.body.insertBefore(editorContainer, null)

  const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        
    ['blockquote', 'code-block'],
    [{'header': 1}, {'header': 2}],
    [{'list': 'ordered'}, {'list': 'bullet'}],
    [{'color': []}, {'background': []}],
    [{'font': []}],
    [{'align': []}],
    ['link', 'image', 'video', 'audio', 'save'] 
  ];

  const editor = new Quill(editorContainer, {
    modules: {
      cursors: true,
      toolbar: {
        container: toolbarOptions,
        handlers: {
          'image': function() {
              selectLocalFile().then(file => {
                  insertToEditor(file, 'image');
              });
          },
          'audio': function() {
              selectLocalFile().then(file => {
                  insertToEditor(file, 'audio');
              });
          },
          'video': function() {
              selectLocalFile().then(file => {
                  insertToEditor(file, 'video');
              });
          },
          'save': function() {
            saveData()
          }
        }
      },
      history: {
        userOnly: true
      }
    },
    placeholder: 'Start collaborating...',
    theme: 'snow' // or 'bubble'
  })

  
  function saveData () {
    //save data logic here
    console.log("Saved!!\n",editor.root.innerHTML);
  }

  function selectLocalFile() {
    return new Promise((resolve, reject) => {
        let input = document.createElement('input');
        input.type = 'file';
        input.onchange = e => {
            resolve(e.target.files[0]);
        };
        input.click();
    });
  }

  function insertToEditor(file, type) {
    let reader = new FileReader();
    reader.onload = function(e) {
        let fileContent = e.target.result;
        let url = "";
        /*
        File content goes to back and from backend a url to access this image is returned
        The url will returnm file content in appropirate content type
        */
        if(type==="image") url = "https://static1.cbrimages.com/wordpress/wp-content/uploads/2023/02/luffy-is-grinning-in-the-movie.jpg";
        else if (type==="video") url="https://static.moewalls.com/videos/preview/2023/zoro-santoryu-ogi-sanzen-sekai-one-piece-preview.mp4";
        else if (type==="audio") url="http://commondatastorage.googleapis.com/codeskulptor-assets/Evillaugh.ogg";
        let range = editor.getSelection();
        if(type==="video") {
            let videoEle = document.createElement('video')
            videoEle.classList.add("ql-video")
            // videoEle.width = "320"
            // videoEle.height = "240"
            videoEle.controls = "true"
            let videoSrc = document.createElement('source')
            videoSrc.src = url
            videoSrc.type = "video/mp4"
            videoEle.appendChild(videoSrc);
            // let videoSrc = `<source src="${url}" type="video/mp4">`
            document.getElementsByClassName('ql-editor')[0].appendChild(videoEle)
        }
        else editor.insertEmbed(range.index, type, url, 'user');
    };
    reader.readAsDataURL(file);
  }

  let AudioBlot = Quill.import('formats/video');

  class AudioBlotCustom extends AudioBlot {
    static create(url) {
        let node = super.create(url);
        node.setAttribute('controls', '');
        return node;
    }
  }
  AudioBlotCustom.blotName = 'audio';
  AudioBlotCustom.tagName = 'audio';
  Quill.register(AudioBlotCustom);

  document.getElementsByClassName('ql-audio')[0].innerHTML = "<i class='fas fa-headset'></i>";
  document.getElementsByClassName('ql-save')[0].innerHTML = "<i class='fas fa-floppy-disk'></i>";

  const binding = new QuillBinding(ytext, editor, provider.awareness)

  /*
  // Define user name and user name
  // Check the quill-cursors package on how to change the way cursors are rendered
  provider.awareness.setLocalStateField('user', {
    name: 'Typing Jimmy',
    color: 'blue'
  })
  */

  // const connectBtn = document.getElementById('y-connect-btn')
  // connectBtn.addEventListener('click', () => {
  //   if (provider.shouldConnect) {
  //     provider.disconnect()
  //     connectBtn.textContent = 'Connect'
  //   } else {
  //     provider.connect()
  //     connectBtn.textContent = 'Disconnect'
  //   }
  // })

  // @ts-ignore
  window.example = { provider, ydoc, ytext, binding, Y }
})
