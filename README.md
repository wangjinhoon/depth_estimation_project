## [**Monocular Depth Estimation through Virtual-world Supervision and Real-world SfM Self-Supervision**](https://arxiv.org/abs/2103.12209)
**Abstract:** Depth information is essential for on-board perception in autonomous driving and driver assistance. Monocular depth estimation (MDE) is very appealing since it allows for appearance and depth being on direct pixelwise correspondence without further calibration. Best MDE models are based on Convolutional Neural Networks (CNNs) trained in a supervised manner, i.e., assuming pixelwise ground truth (GT). Usually, this GT is acquired at training time through a calibrated multi-modal suite of sensors. However, also using only a monocular system at training time is cheaper and more scalable. This is possible by relying on structure-from-motion (SfM) principles to generate self-supervision. Nevertheless, problems of camouflaged objects, visibility changes, static-camera intervals, textureless areas, and scale ambiguity, diminish the usefulness of such self-supervision. In this paper, we perform monocular depth estimation by virtual-world supervision (MonoDEVS) and real-world SfM self-supervision. We compensate the SfM self-supervision limitations by leveraging virtual-world images with accurate semantic and depth supervision and addressing the virtual-to-real domain gap. Our [**MonoDEVSNet**](https://arxiv.org/abs/2103.12209) outperforms previous MDE CNNs trained on monocular and even stereo sequences.


![Alt Text](media/figures/monodevsnet_kitti_seq.gif)


This is an official [**PyTorch**](https://pytorch.org/) implementation of [**Monocular Depth Estimation through Virtual-world Supervision and Real-world SfM Self-Supervision (*Arxiv*)**](https://arxiv.org/abs/2103.12209) 
*Akhil Gurram, Ahmet Faruk Tuna, Fengyi Shen, Onay Urfalioglu, Antonio M. López*.

## How To Use
**Clone** this github repository:
```bash
  git clone https://github.com/HMRC-AEL/MonoDEVSNet.git
  cd MonoDEVSNet
```

**Create conda** environment based on Conda distribution. All dependencies are in [`MonoDEVSNet.yml`](utils/MonoDEVSNet_env.yml) file in utils folder.

```bash
  conda env create -f utils/MonoDEVSNet_env.yml
```

**Environment activation/deactivation**
```bash
  conda activate MonoDEVSNet
  conda deactivate
```

We run our experiments using PyTorch >= 1.5.0, CUDA=10.2, Python=3.8.x


## Training
*Under construction*

## Evaluation

To evaluate MonoDEVSNet models, provide the model/weights folder path and a configuration file name in the command line arguments.

To run evaluation script on [***KITTI***](http://www.cvlibs.net/datasets/kitti/raw_data.php) [*Eigen*](splits/eigen/test_files.txt) split
```bash
    python3 evaluation.py --config <hrnet_w48_vk2> --dataset <kitti> \ 
    --image_folder_path <KITTI_RAW_Dataset_ROOT> \ 
    --load_weights_folder <PATH_TO_MonoDEVSNet_MODELS> \    
    [--version <add_extension_to_save_the_file(rgbs/predicted_depth_maps)>](optional)
```

To run evaluation script on ***any*** images 
```bash
    python3 evaluation.py --config hrnet_w48_vk2 --dataset any \ 
    --image_folder_path <PATH_TO_IMAGES_DIR> \
    --load_weights_folder <PATH_TO_MonoDEVSNet_MODELS>
```

## Models
Download all available MonoDEVSNet models from the [**link**](https://drive.google.com/drive/folders/1_Zbk6AjOcJ34ERlB8mpu5xT84ptbd1Iz?usp=sharing) and place them under MonoDEVSNet/models folder. Rename the each `MODEL` folder name, same as their config-filename.

| MODEL | Virtual dataset | config <br> filename | Abs.Rel. | Sqr.Rel | RMSE | d < 1.25 |
| :---: | :---: | :---: | :---: |  :---: |  :---: |  :---: |
| [MonoDEVSNet HRNet W18](https://drive.google.com/drive/folders/1gvwhFKDLY1I3-V19yCCRfgsIGLxOg4rn?usp=sharing) | [vK 2.0](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds-vkitti-2/) | hrnet_w18_vk2 | 0.109 | 0.773 | 4.524 | 0.871 |
| [MonoDEVSNet HRNet W32](https://drive.google.com/drive/folders/1HMXBew30d4QUgagDQXEPu3lH14kxSVRz?usp=sharing) | [vK 2.0](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds-vkitti-2/) | hrnet_w32_vk2  | 0.107 | 0.754 | 4.510 | 0.875 |
| [MonoDEVSNet HRNet W48](https://drive.google.com/drive/folders/1rt0A-GqGoSnSR2YkpLRySo03I7FGKW_4?usp=sharing) | [vK 1.0](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds-vkitti-1/) | hrnet_w48_vk1  | 0.108 | 0.775 | 4.464 | 0.875 | 
| [MonoDEVSNet HRNet W48](https://drive.google.com/drive/folders/1-Ufc4ChU9LrTtlurq61A-N6B-KP2Nc_R?usp=sharing) | [vK 2.0](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds-vkitti-2/) | hrnet_w48_vk2 | **0.104** | **0.721** | **4.396** | **0.880** |
| [MonoDEVSNet HRNet W48 - simplified](https://drive.google.com/drive/folders/1VgeqWoYFQckxEjeME7TMwLXtBXsq1IFe?usp=sharing) | [vK 2.0](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds-vkitti-2/) | hrnet_w48_vk2_simplified | 0.105 | 0.736 | 4.471 | 0.875 |


## Precomputed depth estimation results

To visualize the MonoDEVSNet results, run 

```bash
  python3 scripts/load_eval_output.py --file_path <PATH_TO_SAVED/DOWNLOADED_FILE>
``` 

| Model | Encoder | Virtual dataset | Link |
| :--- | :---: | :---: | :---: |
| MonoDEVSNet | HRNet W48 | vK 1.0 | [**Download**](https://drive.google.com/file/d/1MpCXKVih-LKFVtQ0Nm4CR53sJpk0T5Ah/view?usp=sharing)
| MonoDEVSNet | HRNet W48 | vK 2.0 | [**Download**](https://drive.google.com/file/d/1DLLyaHVdsmifyFGatzpU4vIvu-CcfR2I/view?usp=sharing)

## Related code

[**monodepth2**](https://github.com/nianticlabs/monodepth2)

## License
The source code is released under the [MIT license](LICENSE.md).

## Cite
If you want to cite the framework feel free to use this preprint citation while we await publication:

**Monocular Depth Estimation through Virtual-world Supervision and Real-world SfM Self-Supervision** [**Arxiv**](https://arxiv.org/abs/2103.12209)

*Akhil Gurram, Ahmet Faruk Tuna, Fengyi Shen, Onay Urfalioglu, Antonio M. López*

```bibtex
@article{gurram2021monocular,
  title={Monocular Depth Estimation through Virtual-world Supervision and Real-world SfM Self-Supervision},
  author={Gurram, Akhil and Tuna, Ahmet Faruk and Shen, Fengyi and Urfalioglu, Onay and L{\'o}pez, Antonio M},
  journal={arXiv preprint arXiv:2103.12209},
  year={2021}
}
```

Contact: akhil.gurram@e-campus.uab.cat
