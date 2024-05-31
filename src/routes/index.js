import express from 'express'
const router = express.Router();
import admin from '../config/firebase';
import firebaseAuthController from '../controllers/firebase-controller';
import verifyToken from '../middleware';


router.post('/api/register', firebaseAuthController.registerUser);
router.post('/api/login', firebaseAuthController.loginUser);
router.post('/api/logout', firebaseAuthController.logoutUser);
router.post('/api/reset-password', firebaseAuthController.resetPassword);
router.get('/api/hello',verifyToken,(req, res)=>{
    return res.send('Hello');
})
export default router;