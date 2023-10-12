# Real-Time Event Prediction
<a name="readme-top"></a>

This repository includes implementation of our studies that propose novel methods for 
real-time event prediction for heterogeneous multivariate temporal data (time series, instantaneous events, and time intervals).


In the animation below, V1 and V2 are time series, V3 represents instantaneous events, and V4 represents time intervals.
The animation shows that the probability of experiencing an event of interest (heart attack here) increases over time (tc represent the current time), while the estimated time to event decreases.

![Real-Time Event Prediction](figures/hetro_event_pred.gif)
![img.png](img.png)
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#background">Background</a>
    </li>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#citations-and-papers">Citations & Papers</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#input-files">Input Files</a></li>
        <li><a href="#config-file">Config File</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- Background -->
## Background
Symbolic time intervals (STIs) are a powerful way to represent time-series data and real-life events with varying duration, such as traffic light timing or medical treatments. STIs can be used to uniformly represent heterogeneous multivariate temporal data (time series, instantaneous events, or time intervals), including both event-driven measurements (e.g., traffic accidents) and manual measurements (e.g., blood tests).
Temporal abstraction can be used to uniformly represent such heterogeneous multivariate temporal data using STIs. 
Frequent time intervals-related patterns (TIRPs) can be discovered from the STI data, which have proven to be valuable for knowledge discovery, as well as for use as features in classification and prediction tasks.

<!-- ABOUT THE PROJECT -->
## About The Project
Our method builds on our previous work on the continuous prediction of a single TIRP completion.
The completion of a TIRP can be inferred by calculating the probability of observing the remaining part of the pattern, given its observed part at a specific time.
We also implemented an extension of the single TIRP completion model to be capable of estimating the TIRP's completion occurrence time, in addition to the completion probability.
By continuously aggregating multiple completion models for TIRPs that end with an event of interest, we learn a continuous event prediction model that is capable of estimating the event's occurrence probability and time.
A model that leverages multiple TIRPs is expected to generalize better than a model that uses a single TIRP.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Citations & Papers -->
## Citations and Papers
Prediction of TIRP completion - PAKDD'2023 (Pacific-Asia Conference on Knowledge Discovery and Data Mining) [[Link](https://dl.acm.org/doi/abs/10.1007/978-3-031-33374-3_19)]:

`Itzhak, N., Jaroszewicz, S., & Moskovitch, R. (2023, May). Continuously predicting the completion of a time intervals related pattern. In Pacific-Asia Conference on Knowledge Discovery and Data Mining (pp. 239-251). Cham: Springer Nature Switzerland.`

Prediction of TIRP completion - Knowledge and Information Systems - Journal version [[Link](https://link.springer.com/article/10.1007/s10115-023-01910-w)]:

`Itzhak, N., Jaroszewicz, S., & Moskovitch, R. (2023). Continuous prediction of a time intervals-related pattern’s completion. Knowledge and Information Systems, 1-50.`


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started


### Input Files

TBD

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Config File

TBD

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

The `requirements.txt` file lists all Python libraries that the project depend on,
and they will be installed using:

 ```sh
 pip install -r requirements.txt
 ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

**The code is divided as follows** 
* The main_cpu.py python file contains the necessary code for running the data creation for the HugoBot system and creating the different representations of the abstract data.

* The main_gpu.py python file contains the necessary code for running the DNN models

* The run_models.py python file called by the main_gpu.py contains the code that is responsible for calling the relevant functions of creating the models

* The **utils_folder** contains the necessary functions to read the datasets, visualize the plots and set the parameters.

* The **classifiers folder** contains 11 python files, one for each deep neural network.

* The **temporal_abstraction_f** Contains the code responsible for the transformation that converts the code to the HugoBot system and for the neural networks.

* **HugoBot system** - performs the process of temporal abstraction


**The flow**
1. Create an anaconda env and install the relevant packages as described below. **Note:** To convert the MTS format from MATLAB  to np: Run the main_cpu.py file with the following parameters - "transform_mts_to_ucr_format".

2. **Create the data for the hugobot system on the CPU cluster:** Run the main_cpu.py  with the following parameters - "create_files_for_hugobot {archive_name} {per_entity}"  
**Note** - The first run must be with per_entity= False

3. **Create the data for the DNN:** Run the main_cpu.py file with the following parameters -  
"create_files {archive_name} {after_TA} {TA_metod} {combination} {transformation_number = 1} {per_entity}"

4. **Running the DNN**  **on the gpu cluster:** Run the main_gpu.py file with the following parameters - "run_all {archive_name} {after_TA} {TA_metod} {combination} {transformation_number} {per_entity}"

5. **Evaluating the results:** Run cd-diagram_graphs.py file or graphs.py file.  
Parameters for the graphs.py:  
The main function is 'create_all_graphs'. The function receives the following params:

	* graph_numbers – list of the graphs you want to create.

	* create_csv (Boolean) – combining all the results of the DNN architectures.  **Note** – this param needs to be set to True only in the first run.

	* type – {archive_name}

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
