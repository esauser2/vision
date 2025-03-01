from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union

import PIL.Image
import torch
from torchvision.transforms.functional import InterpolationMode

from ._datapoint import Datapoint, FillTypeJIT


class Image(Datapoint):
    @classmethod
    def _wrap(cls, tensor: torch.Tensor) -> Image:
        image = tensor.as_subclass(cls)
        return image

    def __new__(
        cls,
        data: Any,
        *,
        dtype: Optional[torch.dtype] = None,
        device: Optional[Union[torch.device, str, int]] = None,
        requires_grad: Optional[bool] = None,
    ) -> Image:
        tensor = cls._to_tensor(data, dtype=dtype, device=device, requires_grad=requires_grad)
        if tensor.ndim < 2:
            raise ValueError
        elif tensor.ndim == 2:
            tensor = tensor.unsqueeze(0)

        return cls._wrap(tensor)

    @classmethod
    def wrap_like(cls, other: Image, tensor: torch.Tensor) -> Image:
        return cls._wrap(tensor)

    def __repr__(self, *, tensor_contents: Any = None) -> str:  # type: ignore[override]
        return self._make_repr()

    @property
    def spatial_size(self) -> Tuple[int, int]:
        return tuple(self.shape[-2:])  # type: ignore[return-value]

    @property
    def num_channels(self) -> int:
        return self.shape[-3]

    def horizontal_flip(self) -> Image:
        output = self._F.horizontal_flip_image_tensor(self.as_subclass(torch.Tensor))
        return Image.wrap_like(self, output)

    def vertical_flip(self) -> Image:
        output = self._F.vertical_flip_image_tensor(self.as_subclass(torch.Tensor))
        return Image.wrap_like(self, output)

    def resize(  # type: ignore[override]
        self,
        size: List[int],
        interpolation: InterpolationMode = InterpolationMode.BILINEAR,
        max_size: Optional[int] = None,
        antialias: Optional[bool] = None,
    ) -> Image:
        output = self._F.resize_image_tensor(
            self.as_subclass(torch.Tensor), size, interpolation=interpolation, max_size=max_size, antialias=antialias
        )
        return Image.wrap_like(self, output)

    def crop(self, top: int, left: int, height: int, width: int) -> Image:
        output = self._F.crop_image_tensor(self.as_subclass(torch.Tensor), top, left, height, width)
        return Image.wrap_like(self, output)

    def center_crop(self, output_size: List[int]) -> Image:
        output = self._F.center_crop_image_tensor(self.as_subclass(torch.Tensor), output_size=output_size)
        return Image.wrap_like(self, output)

    def resized_crop(
        self,
        top: int,
        left: int,
        height: int,
        width: int,
        size: List[int],
        interpolation: InterpolationMode = InterpolationMode.BILINEAR,
        antialias: Optional[bool] = None,
    ) -> Image:
        output = self._F.resized_crop_image_tensor(
            self.as_subclass(torch.Tensor),
            top,
            left,
            height,
            width,
            size=list(size),
            interpolation=interpolation,
            antialias=antialias,
        )
        return Image.wrap_like(self, output)

    def pad(
        self,
        padding: Union[int, List[int]],
        fill: FillTypeJIT = None,
        padding_mode: str = "constant",
    ) -> Image:
        output = self._F.pad_image_tensor(self.as_subclass(torch.Tensor), padding, fill=fill, padding_mode=padding_mode)
        return Image.wrap_like(self, output)

    def rotate(
        self,
        angle: float,
        interpolation: InterpolationMode = InterpolationMode.NEAREST,
        expand: bool = False,
        center: Optional[List[float]] = None,
        fill: FillTypeJIT = None,
    ) -> Image:
        output = self._F.rotate_image_tensor(
            self.as_subclass(torch.Tensor), angle, interpolation=interpolation, expand=expand, fill=fill, center=center
        )
        return Image.wrap_like(self, output)

    def affine(
        self,
        angle: Union[int, float],
        translate: List[float],
        scale: float,
        shear: List[float],
        interpolation: InterpolationMode = InterpolationMode.NEAREST,
        fill: FillTypeJIT = None,
        center: Optional[List[float]] = None,
    ) -> Image:
        output = self._F.affine_image_tensor(
            self.as_subclass(torch.Tensor),
            angle,
            translate=translate,
            scale=scale,
            shear=shear,
            interpolation=interpolation,
            fill=fill,
            center=center,
        )
        return Image.wrap_like(self, output)

    def perspective(
        self,
        startpoints: Optional[List[List[int]]],
        endpoints: Optional[List[List[int]]],
        interpolation: InterpolationMode = InterpolationMode.BILINEAR,
        fill: FillTypeJIT = None,
        coefficients: Optional[List[float]] = None,
    ) -> Image:
        output = self._F.perspective_image_tensor(
            self.as_subclass(torch.Tensor),
            startpoints,
            endpoints,
            interpolation=interpolation,
            fill=fill,
            coefficients=coefficients,
        )
        return Image.wrap_like(self, output)

    def elastic(
        self,
        displacement: torch.Tensor,
        interpolation: InterpolationMode = InterpolationMode.BILINEAR,
        fill: FillTypeJIT = None,
    ) -> Image:
        output = self._F.elastic_image_tensor(
            self.as_subclass(torch.Tensor), displacement, interpolation=interpolation, fill=fill
        )
        return Image.wrap_like(self, output)

    def rgb_to_grayscale(self, num_output_channels: int = 1) -> Image:
        output = self._F.rgb_to_grayscale_image_tensor(
            self.as_subclass(torch.Tensor), num_output_channels=num_output_channels
        )
        return Image.wrap_like(self, output)

    def adjust_brightness(self, brightness_factor: float) -> Image:
        output = self._F.adjust_brightness_image_tensor(
            self.as_subclass(torch.Tensor), brightness_factor=brightness_factor
        )
        return Image.wrap_like(self, output)

    def adjust_saturation(self, saturation_factor: float) -> Image:
        output = self._F.adjust_saturation_image_tensor(
            self.as_subclass(torch.Tensor), saturation_factor=saturation_factor
        )
        return Image.wrap_like(self, output)

    def adjust_contrast(self, contrast_factor: float) -> Image:
        output = self._F.adjust_contrast_image_tensor(self.as_subclass(torch.Tensor), contrast_factor=contrast_factor)
        return Image.wrap_like(self, output)

    def adjust_sharpness(self, sharpness_factor: float) -> Image:
        output = self._F.adjust_sharpness_image_tensor(
            self.as_subclass(torch.Tensor), sharpness_factor=sharpness_factor
        )
        return Image.wrap_like(self, output)

    def adjust_hue(self, hue_factor: float) -> Image:
        output = self._F.adjust_hue_image_tensor(self.as_subclass(torch.Tensor), hue_factor=hue_factor)
        return Image.wrap_like(self, output)

    def adjust_gamma(self, gamma: float, gain: float = 1) -> Image:
        output = self._F.adjust_gamma_image_tensor(self.as_subclass(torch.Tensor), gamma=gamma, gain=gain)
        return Image.wrap_like(self, output)

    def posterize(self, bits: int) -> Image:
        output = self._F.posterize_image_tensor(self.as_subclass(torch.Tensor), bits=bits)
        return Image.wrap_like(self, output)

    def solarize(self, threshold: float) -> Image:
        output = self._F.solarize_image_tensor(self.as_subclass(torch.Tensor), threshold=threshold)
        return Image.wrap_like(self, output)

    def autocontrast(self) -> Image:
        output = self._F.autocontrast_image_tensor(self.as_subclass(torch.Tensor))
        return Image.wrap_like(self, output)

    def equalize(self) -> Image:
        output = self._F.equalize_image_tensor(self.as_subclass(torch.Tensor))
        return Image.wrap_like(self, output)

    def invert(self) -> Image:
        output = self._F.invert_image_tensor(self.as_subclass(torch.Tensor))
        return Image.wrap_like(self, output)

    def gaussian_blur(self, kernel_size: List[int], sigma: Optional[List[float]] = None) -> Image:
        output = self._F.gaussian_blur_image_tensor(
            self.as_subclass(torch.Tensor), kernel_size=kernel_size, sigma=sigma
        )
        return Image.wrap_like(self, output)

    def normalize(self, mean: List[float], std: List[float], inplace: bool = False) -> Image:
        output = self._F.normalize_image_tensor(self.as_subclass(torch.Tensor), mean=mean, std=std, inplace=inplace)
        return Image.wrap_like(self, output)


ImageType = Union[torch.Tensor, PIL.Image.Image, Image]
ImageTypeJIT = torch.Tensor
TensorImageType = Union[torch.Tensor, Image]
TensorImageTypeJIT = torch.Tensor
