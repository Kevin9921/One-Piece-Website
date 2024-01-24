import React, {useEffect, useState} from 'react'
//import { getStorage } from "firebase/storage";
import { initializeApp } from 'firebase/app';
import { getStorage, ref, getDownloadURL } from 'firebase/storage';
import './App.css';
import { CountdownCircleTimer } from 'react-countdown-circle-timer'



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
  const [name, setName] = useState("");
  const [timer, setTimer] = useState(); 
  const [points, setPoints] = useState(0);
 

  const renderTime = ({ remainingTime }) => {
    // if (remainingTime === 0) {
    //   return <div className="timer">Too lale...</div>;
    // }
  
    return (
      <div className="timer">

        <div className="value">{remainingTime}</div>
       
      </div>
    );
  };

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
    const interval = setInterval(() => {
      setTimer((prevTimer) => (prevTimer > 0 ? prevTimer - 1 : 0));
    }, 1000);

    // Cleanup the interval when the component is unmounted or timer reaches 0
    return () => clearInterval(interval);
  }, [backendData]);


  const handleInputChange = (e, row) => {
   
    const inputValue = e.target.value;
    setName(inputValue); // Update the name state
    console.log(inputValue)

    // Check if the input value matches the current row's name
    if (row && row.name && inputValue.toLowerCase() === row.name.toLowerCase()) {
      setPoints((prevPoints) => prevPoints + 1);
      handleNewCharacter()
      console.log("working");
  }
  };

  const handleNewCharacter = () => {
    // Send a request to the server to get a new character
    fetch("/api/newCharacter")
      .then((response) => response.json())
      .then((data) => {
        // Update the state with the new character data
        setBackendData(data);
      
      })
      .catch((error) => console.error("Error fetching new character:", error));
  };

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
            
                
                <p>Name: {row.name}</p>
                <img className='characterImage' 
                
                  // src="/character_images/Ace.jpg"
                  src={row.image_url}
                  alt={row.name} 
                  // style={{ maxWidth: '300px', maxHeight: '300px' }} 
                />
                <div className="timer-wrapper">
                  <CountdownCircleTimer
                    isPlaying
                    duration={10}
                    colors={["#7cfc00", "#F7B801", "#A30000", "#A30000"]}
                    colorsTime={[10, 6, 3, 0]}
                    onComplete={() => ({ shouldRepeat: true, delay: 1 })}
                    size = {60}
                    strokeWidth = {5}
                  >
                    {renderTime}
                  </CountdownCircleTimer>
               
                  <p className='points'> {points}</p>
                </div>
                
                <input className='inputBox'
                  type="text" 
                  value={name}
                  onChange={(e) => {
                    console.log(row)
                    handleInputChange(e, row)}} /* Pass the current row to the handler */
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