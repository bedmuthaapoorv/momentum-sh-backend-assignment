import admin from 'firebase-admin'
import firebase from 'firebase/compat/app';

import serviceAccount from '../momentumsh-assignment-firebase-adminsdk-zje2r-f298e0b887.json' assert { type: "json" }
const firebaseConfig = {
    apiKey: "AIzaSyBdk7pJDAJIXMBSHFvEb0d7VMFqes7GGXA",
    authDomain: "momentumsh-assignment.firebaseapp.com",
    projectId: "momentumsh-assignment",
    storageBucket: "momentumsh-assignment.appspot.com",
    messagingSenderId: "702432799934",
    appId: "1:702432799934:web:b81b4059a4e1c1a54f42ef"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
})

export default admin;