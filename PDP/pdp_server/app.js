import express from 'express';
import path from 'path';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import createError from 'http-errors';
import cors from 'cors';
import { fileURLToPath } from 'url';

import indexRouter from './routes/index.js';
import usersRouter from './routes/users.js';
import fidoRouter from './routes/fido.js';
import fidoRouter1 from './routes/web_fido.js';
import RPRouter from './routes/rp.js';
import RPMaintainRouter from './routes/rp_maintained.js' ; 

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();


// 設置 view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// 設定 CORS 選項
const corsOptions = {
  origin: ['https://ag.yuntech.poc.com:8080','https://ag.yuntech.poc.com', 'http://de.yuntech.poc.com', 'http://de.yuntech.poc.com:3001'], // 允許的來源，可以是多個
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], // 允許的 HTTP 方法
  allowedHeaders: ['Content-Type', 'Authorization'], // 允許的 HTTP 頭部
  credentials: true, // 如果需要傳遞憑證（如 Cookies），設置為 true
};

app.use(cors(corsOptions));

// 中間件
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// 路由
app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/agentfido', fidoRouter);
app.use('/webfido', fidoRouter1);
app.use('/rp' , RPRouter);
app.use('/maintained-computers' , RPMaintainRouter)

// 捕獲 404 並轉交到錯誤處理器
app.use(function(req, res, next) {
  next(createError(404));
});

// 錯誤處理
app.use(function(err, req, res, next) {
  // 只在開發環境下提供詳細錯誤訊息
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // 顯示錯誤頁面
  res.status(err.status || 500);
  res.render('error');
});

export default app;
