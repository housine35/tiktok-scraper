## TikTok Scraper

A FastAPI-based web application to scrape TikTok data, including posts, followers, following, and comments, and save the results to Excel files. This project uses Playwright for browser automation to handle TikTok's URL signing requirements.

## Features
- Scrape TikTok posts, followers, following, and comments for a given user.
- Save scraped data to Excel files with multiple sheets for different data types.
- Built with FastAPI for a robust and scalable API.
- Uses Playwright for browser automation to generate signed URLs.
- Containerized with Docker for easy deployment.

## Prerequisites
- Docker and Docker Compose (for containerized deployment)
- Node.js (v18 or later) and npm (for local development)
- Python (3.12 or later) and pip (for local development)
- A TikTok account for testing (e.g., @movedz)

## Installation
- Using Docker (Recommended)
- Clone the repository:
- git clone https://github.com/your-username/tiktok-scraper.git
- cd tiktok-scraper
- Build and run the Docker container:
    docker-compose build
    docker-compose up
The API will be available at http://localhost:8000.

## Response:
A downloadable Excel file containing the scraped data, organized into sheets (e.g., "Posts", "Followers", etc.).

Check the logs for debugging information (enabled with --log-level debug).

Python: FastAPI, pandas, openpyxl, requests, uvicorn

Node.js: Playwright (v1.48.1)

Docker: For containerized deployment

## Troubleshooting
- Error: Cannot find module '/app/services/validUrl.js':
- Ensure docker-compose.yaml mounts the project directory correctly (./:/app).
- Verify that app/services/validUrl.js exists in the project directory.
- Error: Host system is missing dependencies to run browsers:
- The Dockerfile includes npx playwright install-deps to install all necessary system dependencies.

## License

This project is licensed under the ISC License. See the package.json for details.

Contact

For questions or issues, please open an issue on GitHub or contact the maintainer at [housine35@hotmail.com].
