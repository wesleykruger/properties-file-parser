# properties-file-parser

Simple script that arose from a business need to extract Cron job schedules from properties files containing thousands of lines of non-relevant configuration.

This may or may not work as-is for other properties files, as it requries a specific format where the target cron jobs always follow a comment section beginning with #Group=*;Cron job syntax. It should be fairly simple to adjust as needed, though.
