# EPL-Card-Reader-Interface

The capstone project for Portland State Universities EPL Card Reader project. An interface an admin can interact with to verify or update student's "trained" status for various ECE machines in ECE labs. It will offer portability and flexibility so that it may be used across multiple labs at PSU.

Per the Sponsor's request:
The EPL is seeking a streamlined check in system for students entering the lab. This system would build on the previous ECE capstone RFID badge reader system sponsored by the EPL. At check in, on scanning their student ID, the user interface displays an iconographic grid indicating wether a student is trained to use various equipment categories around the lab. The icons would change color to indicate status. 

This system would also facilitate and track safety waivers and emergency contact status for quick retrieval by an EPL manager in case of emergency. EPL managers will be able to mark a person as trained (per icon) in the system.

This system should be easily reconfigurable in the UI for different shops around campus. 

I would guess that it may make the most sense to host on a local server. I would however, like to make it easy to stand it up on a PC with the UI pointed at the 127.0.0.1:x so that it could have a standalone mode as well. 


Pending hardware specs, currently planning on the following framework:

- Server webdev in Rust using the Rocket framework
- An SQL database
- The Diesel library for the query tool
- REACT Hook for front end

