import { createLogger, transports, format } from 'winston';

const winlogger = createLogger({
    transports: [
        new transports.File({
            filename: "logs/server.log",
            level: "info",
            format: format.combine(
                format.align(),
                format.printf(
                    (info) =>
                        `${info.level}: ${info.message}` 
                )
            )
        })
    ]
});

export default winlogger;