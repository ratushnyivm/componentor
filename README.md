<div align="center">

# componentor

[![CI](https://github.com/ratushnyyvm/componentor/actions/workflows/CI.yml/badge.svg)](https://github.com/ratushnyyvm/componentor/actions/workflows/CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/6be55a5ee170e20da5b7/maintainability)](https://codeclimate.com/github/ratushnyyvm/componentor/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6be55a5ee170e20da5b7/test_coverage)](https://codeclimate.com/github/ratushnyyvm/componentor/test_coverage)

</div>

---

## Demo

The demo version is available at http://195.133.146.77/

---

## Description

A small archive for the design department. Allows searching for parts in an
assembly by material.

---

## Dependencies

| Tool          | Version  |
|---------------|----------|
| python        | "^3.11"  |
| django        | "^4.2.1" |
| python-dotenv | "^1.0.0" |

---

## Installation

Make sure that you have [Docker](https://docs.docker.com/desktop/)
and [Docker Compose](https://docs.docker.com/compose/) installed.

1. Clone this repository

    ```bash
    git clone https://github.com/ratushnyyvm/componentor.git && cd componentor
    ```

2. Rename `.env.example` file to `.env` and enter `SECRET_KEY`

    ```bash
    SECRET_KEY=your_secret_key
    ```

3. Run
    ```bash
    docker-compose up
   ```

The server is running at http://0.0.0.0:8000.

---

## Usage

Users have access to creating, viewing, updating, and deleting materials, parts,
and assemblies.  
List pages have filters available for quick searching.  
When creating parts and assemblies, there is a search window available for
quickly selecting the required component.
