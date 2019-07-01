# Parliamentary transparency



## Install requirements

`pip install -r requirements.txt`



## Project structure

There are two main folders in the project.

In the **data_explore** folder we have all files on data collection and processing.

In the **parlamentar** folder we have the [Lektor](https://www.getlektor.com/) project to create the website.



### Render the website 

To run a local service with the website go to the **parlamentar** folder and run:

`lektor serve`

You can change the port using:

`lektor serve -p $port_number`

To generate all the static files for the project you can run:

`lektor built`

But if you run `lektor serve` the build is already done automatically while you perform any change to the code.

Full documentation for Lektor can be found at [https://www.getlektor.com](https://www.getlektor.com).

