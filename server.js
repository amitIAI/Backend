require('dotenv').config();
const express = require('express');
const cors = require("cors");
const { google } = require('googleapis');
const fs = require('fs');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 5000;

// ✅ Enable CORS (Add this before defining routes)
app.use(cors());
app.use(express.json()); // Ensure JSON parsing

// Google Drive Authentication Setup
const oauth2Client = new google.auth.OAuth2(
    process.env.CLIENT_ID,
    process.env.CLIENT_SECRET,
    process.env.REDIRECT_URI
);
oauth2Client.setCredentials({ refresh_token: process.env.REFRESH_TOKEN });

const drive = google.drive({ version: 'v3', auth: oauth2Client });

// Multer setup for file uploads
const upload = multer({ dest: 'uploads/' });

app.get('/', (req, res) => {
    res.send('Google Drive API Backend is Running!');
});

// 1. Upload a file to the shared Google Drive folder
app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            throw new Error("No file uploaded.");
        }

        console.log("Uploading file:", req.file.originalname);

        const folderId = process.env.SHARED_FOLDER_ID;
        const fileMetadata = {
            name: req.file.originalname,
            parents: [folderId],
        };
        const media = {
            mimeType: req.file.mimetype,
            body: fs.createReadStream(req.file.path),
        };

        // Upload file to Google Drive
        const file = await drive.files.create({
            resource: fileMetadata,
            media: media,
            fields: 'id, name, parents, mimeType',
        });
        fs.unlinkSync(req.file.path); // Remove local file after upload

        // Fetch folder metadata (Get folder name)
        const folderInfo = await drive.files.get({ fileId: folderId, fields: 'name' });

        res.json({ 
            message: 'File uploaded successfully', 
            fileId: file.data.id, 
            fileName: file.data.name,
            folderName: folderInfo.data.name 
        });

    } catch (error) {
        console.error("Upload error:", error);  // 🔥 Logs detailed error
        res.status(500).json({ error: error.message });
    }
});

// 2. Read a file's content and metadata
app.get('/file/:fileId', async (req, res) => {
    try {
        const { fileId } = req.params;
        const fileMetadata = await drive.files.get({ fileId, fields: 'id, name, mimeType, size, modifiedTime' });
        const fileStream = await drive.files.get({ fileId, alt: 'media' }, { responseType: 'stream' });
        
        let content = '';
        fileStream.data.on('data', (chunk) => (content += chunk));
        fileStream.data.on('end', () => {
            res.json({ metadata: fileMetadata.data, content });
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 3. Get storage space info & warning status
app.get('/storage', async (req, res) => {
    try {
        const { data } = await drive.about.get({ fields: 'storageQuota' });
        const totalSpaceGB = (data.storageQuota.limit / (1024 ** 3)).toFixed(2);
        const usedSpaceGB = (data.storageQuota.usage / (1024 ** 3)).toFixed(2);
        const unusedSpace = ((data.storageQuota.limit - data.storageQuota.usage) / data.storageQuota.limit) * 100;
        let spaceWarning = 'bg-texl';
        if (unusedSpace <= 30) spaceWarning = 'bg-warning';
        if (unusedSpace <= 10) spaceWarning = 'bg-danger';

        res.json({ totalSpaceGB, usedSpaceGB, spaceWarning });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, () => console.log(`Server running on port ${port}`));
