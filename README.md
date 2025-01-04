# Park Smart 🚗🅿️

<div align="center">
    <img height="400" width="400" alt="logo" src="https://github.com/user-attachments/assets/4b06aeb5-3351-46ee-8735-d0fc8bace13e" />
</div>


**Park Smart** is an innovative IoT application designed for parking lot owners to efficiently monitor and manage their parking lots. The system offers real-time data on car entries, parking space availability, and traffic control using smart indicators, while also providing a detailed history of parking usage.

----------

## 🌟 Key Features

-   **Real-time Monitoring**: Tracks cars entering the lot and parking space usage.
-   **Traffic Control**: Uses red and green LEDs to guide vehicles into the lot.
-   **History Logs**: Maintains a record of parking space occupancy.
-   **User Authentication**: Secure Google OAuth login for access.
-   **Role-Based Access**: Differentiated permissions for monitoring and control.

----------

## 📊 System Architecture

The following diagram illustrates the data flow within the system:

<img width="800" alt="system_architecture" src="https://github.com/user-attachments/assets/ff8a8aac-3d03-46fa-bdb0-86f7b91ad723" />

----------

## 🔧 Hardware Components

The system uses the following sensors and actuators:

1.  [**Ultrasonic Sensor**](https://thepihut.com/products/ultrasonic-distance-sensor-hcsr04?variant=1054704288): Detects cars at specific parking spaces.
2.  [**IR Beam Breaker**](https://thepihut.com/products/ir-break-beam-sensor-3mm-leds?variant=27739767825): Counts cars entering the parking lot.
3.  [**Red LED**](https://thepihut.com/products/ultra-bright-led-5mm-red-10-pack?variant=20063184879678): Signals traffic to stop when the parking lot is full.
4.  [**Green LED**](https://thepihut.com/products/ultra-bright-led-5mm-green-10-pack?variant=20063184748606): Signals traffic to proceed when parking spaces are available.

----------

## 🖥️ Hardware Setup

The sensors and actuators are connected to a Raspberry Pi, ensuring security by disabling unused pins and ports. Below is the Fritzing diagram representing the hardware setup:

<img width="800" alt="fritzing" src="https://github.com/user-attachments/assets/b1aaa0e1-ea29-42f5-9b83-67661ab5e2c6" />

----------

## 🌐 Web Application

### Web Server

-   Built with Python, the webserver defines secure routes and is hosted on AWS.
-   The app uses a custom HTTPS-secured domain: [](https://www.parksmart.live/)[https://www.parksmart.live](https://www.parksmart.live).

### Frontend

-   Developed using **HTML**, **DaisyUI (**Tailwind CSS**)**, and **JavaScript** for a responsive and intuitive user experience.

### Authentication

-   Google OAuth integration ensures secure user authentication.
-   Unauthorized access is prevented with route protection using a `login_required` wrapper.
<img width="800" alt="google_auth" src="https://github.com/user-attachments/assets/32280faa-4fde-4afe-9bbc-38c3f2034ab2" />
<img width="800" alt="access_forbidden" src="https://github.com/user-attachments/assets/06df21a9-b395-4e22-bd93-d48c84e1f123" />

----------

## 📡 Real-Time Communication with PubNub

Park Smart uses **PubNub** for real-time data publishing and subscribing.

### 1. **Data Security**
All data in transit is encrypted with a cipher key.

<div align="center">
    <img width="800" alt="access_manager" src="https://github.com/user-attachments/assets/fa7ed3af-74d2-4517-aefd-b7e6aceeafc5" />
</div>

---

### 2. **Access Control**
<img width="800" alt="subscriptions" src="https://github.com/user-attachments/assets/821b169f-7868-4b72-92f4-9540d33b95eb" />

- **Read**: Users can only monitor parking spaces.  
<div align="center">
    <img width="800" alt="standard_subs" src="https://github.com/user-attachments/assets/e5e70420-b286-4b92-92a1-ae3b0f023a29" />
</div>

- **Read and Write**: Users can control LEDs remotely (e.g., during maintenance).  
<div align="center">
    <img width="800" alt="elite_subs" src="https://github.com/user-attachments/assets/c2f4dd51-cd5b-4dc3-aca8-7f19ff3a92bc" />
</div>

- **None**: No access.  
<div align="center">
    <img width="800" alt="no_subs" src="https://github.com/user-attachments/assets/d2e55cb9-c834-4b48-91de-f1230c3b8aa1" />
</div>

Only admins can revoke user access levels.  
<div align="center">
    <img width="800" alt="admin_panel" src="https://github.com/user-attachments/assets/417df024-5b45-41ff-89e6-4b5979a90cb2" />
</div>

----------

## 🛢️ Database Design

All data is securely stored in a **MySQL database**, which includes the following tables:

### `user` Table

Stores user information:

```sql
id, name, client_id, token TEXT, login, read_access, write_access, email

```

### `parking_lot` Table

Tracks parking space occupancy:

```sql
id, user_id, parking_spot, status, timestamp

```

-   Secrets and credentials are stored securely in `.env` files.
-   Database access is secured with triggers and role-based permissions.
<div align="center">
    <img width="800" alt="frontend_database" src="https://github.com/user-attachments/assets/bffb30fa-1635-4fd0-8ea1-20a7aa5a7593" style="display: inline-block; margin-right: 10px;" />
    <img width="800" alt="database" src="https://github.com/user-attachments/assets/53b6a88b-b7db-42b0-a078-0f9493a2651c" style="display: inline-block;" />
</div>


----------

## 🛠️ Technologies Used

-   **Hardware**: Raspberry Pi, Ultrasonic Sensor, IR Beam Breaker, LEDs
-   **Backend**: Python, Flask, MySQL
-   **Frontend**: HTML, Tailwind CSS, JavaScript
-   **Authentication**: Google OAuth
-   **Real-Time Communication**: PubNub
-   **Hosting**: AWS

----------

## 🚧 Known Issues

1.  **Car Exit Monitoring**: An additional IR Beam Breaker is needed to count cars exiting the parking lot.
2.  **AWS Stability**: The AWS instance occasionally crashes. A swap file was created to mitigate the issue by using hard disk space.

----------

## 🎯 Future Enhancements

-   Implement a car exit monitoring system to provide more accurate data on parking lot occupancy.
