# 386_finalProject

**Goal**
To design and construct a voice assistant that when notified, records a sentece asking for weather at a certain sport and returns weather at that spot.

**Project Description** 
This project incorporated many devices including: RaspberryPi, GPU, LLM, and the website wttr.in. There were two main files that were made, a server and a client. The server in this project is the whisper.py file and the client is the gpio.py file.
 The first step in this project was to create the client file. This is where I wrote three functions to transcribe audio to text, process text for wttr.in to understand, and a created a function to return the weather. Then I worked on the server file to build a model pipeline and define a FastAPI endpoint that would receive audio data, process it, and return a transcription of the spoken content. 

**Integration**
The client file held the majority of my code. First, I needed to write a LLM engineering prompt to convert a sentence that requests the weather into the format that wttr.in can process. Next, I had to showcase that I could use the GPIO to trigger an action which in this case was printing to the screen, "Waiting on GPIO." This involved hooking up the button to my breadboard and Pi. Since I used the Pi, it already had an internal pull-down resistor so all I needed to do was attach a wire to ground and to the 3.3V. In order for this to work, I had to call the function on the rising edge which would alert GPIO HIGH and start recording. I then added in a record_audio() function from ICE3 to record audio for four seconds. As stated above, I wrote three other functions. The first one was named voice_to_text() which would POST to whisper.py and convert audio to return text. The second function was named LLM_process which POST to gemma3 that was already provided to us to process text that wttr.in could understand. Finally, the last function was get_weather() that would GET the wttr.in url at a certain spot to return the weather. Once this was completed, a pressed() function was created that would call all the functions and print them. This
was called in my main function. For the server file, I used code from ICE3 to build the pipeline and modify the FastAPI endpoint code. 

**How to Use** 
The first step is to run FastAPI in the server. Once that is properly running, run the code in the client. It will state "Waiting on GPIO" which is waiting for the user to push the button on the breadboard. Once the button is pushed, the client will respond with "Recording..." This tells the user that the Pi is recording audio and to start the message. Once you ask where the weather is in a certain spot, the server will produce a 200 if it's a successful input or a 422 if there is a validation error. If the server producess a 200, then the client will print the weather to the screen.

**Documentation Statement:**
 Used ChatGPT to assist me with the get_weather() function. Chat helped me understand how to use the try part of the function. I also used chat to help me understand how to rewrite the function voice_to_text to get the output from JSON to plain text. Capt Yarbrough helped me a lot with creating the system diagrams, hooking up my buttons, incorperating my functions, and fixing any issues that I encountered. Thank you Capt Yarbrough!!!!
