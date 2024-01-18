import React, {useEffect, useState} from 'react'
//import { getStorage } from "firebase/storage";
import { initializeApp } from 'firebase/app';
import { getStorage, ref, getDownloadURL } from 'firebase/storage';
import './App.css';



// import { initializeApp } from 'firebase/app';
// import { getStorage } from 'firebase/storage';

// Initialize Firebase with your project config
// databaseURL: "https://one-piece-f51db-default-rtdb.firebaseio.com",
const firebaseConfig = {
  apiKey: process.env.REACT_APP_API,
  authDomain: process.env.REACT_APP_AUTH_DOMAIN,
  databaseURL: process.env.REACT_APP_DATABASE,
  projectId: process.env.REACT_APP_PROJECT_ID,
  storageBucket: process.env.REACT_APP_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_APP_ID,
  appId: process.env.REACT_APP_APP_ID,
  measurementId: process.env.REACT_APP_MEASUREMENT_ID
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
const storage = getStorage(firebaseApp);

// const app = initializeApp(firebaseConfig);
// const storage = getStorage(app);

function App() {
  const [backendData, setBackendData] = useState([])
  const [imageURL, setImageURL] = useState('');

  useEffect(() => {
    fetch("/api").then(
      response => response.json()
    ).then(
      data => {
        setBackendData(data)
      }
    )
  }, [])

  // useEffect(() => {
  //   const storageRef = ref(storage, '/character_images/Ace.jpg');

  //   getDownloadURL(storageRef)
  //     .then((url) => {
  //       setImageURL(url);
  //     })
  //     .catch((error) => {
  //       console.error('Error retrieving download URL:', error);
  //     });
  // }, []);
  // const getFirebaseImageURL = async (imagePath) => {
  //   const storageRef = ref(storage, imagePath);
  //   try {
  //     const url = await getDownloadURL(storageRef);
  //     return url;
  //   } catch (error) {
  //     console.error('Error retrieving download URL:', error);
  //     return ''; // Return a placeholder or handle the error appropriately
  //   }
  // };
  const getImageURLs = async () => {
    const imageURLs = await Promise.all(
      backendData.map(async (row) => {
        const storageRef = ref(storage, row.image_url);
        try {
          const url = await getDownloadURL(storageRef);
          return url;
        } catch (error) {
          console.error('Error retrieving download URL:', error);
          return ''; // Return a placeholder or handle the error appropriately
        }
      })
    );

    return imageURLs;
  };

  useEffect(() => {
    getImageURLs().then((imageURLs) => {
      setBackendData((prevData) =>
        prevData.map((row, index) => ({ ...row, imageURL: imageURLs[index] }))
      );
    });
  }, [backendData]);

//   const storage = getStorage(app);

// const storageRef = ref(storage, "images/" + imageName);

// const url = await getDownloadURL(storageRef)
  return (
    <div>
      {(typeof backendData === 'undefined') ? (
        <p>Loading...</p>
      ):(
        backendData.map((row, i) => {
         // const imageUrl = "/character_images/Ace.jpg"; // Adjust based on your backend data
   
          //const imageUrl = `https://storage.googleapis.com/one_piece_images/${row.image_url}`;

         
          //console.log('Image Path:', imagePath);
          return(
            <div className='screen'>

              <div className='characterContainer' key={i}>
            
                
          
                <img className='characterImage' 
                
                  // src="/character_images/Ace.jpg"
                  src={row.image_url}
                  alt={row.name} 
                  // style={{ maxWidth: '300px', maxHeight: '300px' }} 
                  />
                
                <input className='inputBox'
                  type="text" 
    
              />
                {/* console.log(`C:\\Users\\kevin\\projects\\Website\\ ${row.image_url}`) */}
              </div>
            </div>
        )
      })
    )}
    </div>
  )
}

export default App