# Eye_tracking

OKN or Optokinetic Nystagmus is the small eye movement that occurs by the tracking of a moving field. The small back and forth movement of the eye produces a pattern that determines how clearly an individual can observe moving dots across a screen. 

Using Raspberry Pi 4 Model B, we have written code that will track the movement of the pupil and log the x values on an excel spreadsheet. The data is then plotted on a graph which displays an OKN pattern.

Through the use of the Raspberry Pi 4 Model B, we have created a cheaper version of the software that can be more accessible to a greater number of people. Our goal is to track the movement of the eye as it moves in the x direction. 

We started by using a pre-existing video that consisted of an eye with frequent movement. 

The video was converted into greyscale to make the black area (pupil) more visible. 

The code developed tracked the darkest part of the video which was the pupil. This was done using threshold where the black sections were outlined with contours to demonstrate a visual representation. 

The Gaussian blur made the image smooth so that the image was less pixilated and easier to track.

Lines were placed along the x and y axis to show where the centre on the pupil was.

Our next step was to use a live camera rather than a recording. This is more accurate to how the testing would take place in real life. 

The user is able to use any camera, rather than just the pi camera. This allows for more flexible use of the software and wider access to more people. The x and y positions are displayed on the live video to show eye movement in the x and y direction. 

This x position data is logged onto an excel spreadsheet and then plotted onto a graph. The graph demonstrates the OKN pattern that is typically observed when running similar tests.
