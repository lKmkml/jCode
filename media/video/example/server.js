const express = require("express");
const app = express();
const fs = require("fs");
const path = require('path');
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;
const jwt = require('jsonwebtoken');

app.get("/video", function (req, res) {
    const range = req.headers.range;
    if (!range) {
        res.status(400).send("Requires Range header");
    }
    const videoPath = path.join(__dirname + '/jCodeENV/jCode'+req.query.videoname);
    // console.log(videoPath);
    const videoSize = fs.statSync(videoPath).size;
    const CHUNK_SIZE = 10 ** 6;
    const start = Number(range.replace(/\D/g, ""));
    const end = Math.min(start + CHUNK_SIZE, videoSize - 1);
    const contentLength = end - start + 1;
    const headers = {
        "Content-Range": `bytes ${start}-${end}/${videoSize}`,
        "Accept-Ranges": "bytes",
        "Content-Length": contentLength,
        "Content-Type": "video/mp4",
    };
    res.writeHead(206, headers);
    let secret = 'django-insecure-co&qhn&q2*%rg3491&*5#l9ts=fj2$a^mcha)h1_76n8hfg%dc'
    let token = req.query.token
    console.log(token)
    jwt.verify(token, secret, (err, data) => {
        if(err){
          console.log(err);
          res.status(401).send('Unauthorized');
        }
        else{
          console.log(data);
          console.log(new Date().toString());
          const videoStream = fs.createReadStream(videoPath, { start, end });
          videoStream.pipe(res);
        }
    })
    
});
if (cluster.isMaster) {
    for (var i = 0; i < numCPUs; i++) {
      cluster.fork();
    }
    
    cluster.on('exit', (worker, code, signal) => {
      console.log(`worker ${worker.process.pid} died`);
    });
  
} else {
    app.listen(5000, function () {
      console.log('Video streaming server listening on port 5000!');
    });
}


