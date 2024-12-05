import math
import threading
import time
from typing import List, Optional

import click
import httpx
from tqdm import tqdm

from ..commands.token import ensure_token

# Comprehensive list of allowed styles
ALLOWED_STYLES: List[str] = [
    # Realistic Image Styles
    "any",
    "realistic_image",
    "realistic_image_mockup",
    "realistic_image_b_and_w",
    "realistic_image_enterprise",
    "realistic_image_hard_flash",
    "realistic_image_hdr",
    "realistic_image_natural_light",
    "realistic_image_studio_portrait",
    "realistic_image_motion_blur",
    "realistic_image_evening_light",
    "realistic_image_faded_nostalgia",
    "realistic_image_forest_life",
    "realistic_image_golden_hues",
    "realistic_image_intensity_hue",
    "realistic_image_mystic_naturalism",
    "realistic_image_natural_tones",
    "realistic_image_nightlife_shine",
    "realistic_image_organic_calm",
    "realistic_image_real_life_glow",
    "realistic_image_retro_realism",
    "realistic_image_retro_snapshot",
    "realistic_image_serene_fogscape",
    "realistic_image_urban_drama",
    "realistic_image_village_realism",
    "realistic_image_warm_folk",
    # Digital Illustration Styles
    "digital_illustration",
    "illustration_3d",
    "digital_illustration_seamless",
    "digital_illustration_pixel_art",
    "digital_illustration_3d",
    "digital_illustration_psychedelic",
    "digital_illustration_hand_drawn",
    "digital_illustration_grain",
    "digital_illustration_glow",
    "digital_illustration_80s",
    "digital_illustration_watercolor",
    "digital_illustration_voxel",
    "digital_illustration_infantile_sketch",
    "digital_illustration_2d_art_poster",
    "digital_illustration_kawaii",
    "digital_illustration_halloween_drawings",
    "digital_illustration_2d_art_poster_2",
    "digital_illustration_engraving_color",
    "digital_illustration_flat_air_art",
    "digital_illustration_hand_drawn_outline",
    "digital_illustration_handmade_3d",
    "digital_illustration_stickers_drawings",
    "digital_illustration_antiquarian",
    "digital_illustration_bold_fantasy",
    "digital_illustration_child_book",
    "digital_illustration_child_books",
    "digital_illustration_cover",
    "digital_illustration_crosshatch",
    "digital_illustration_digital_engraving",
    "digital_illustration_dreamlike_hues",
    "digital_illustration_expressionism",
    "digital_illustration_freehand_details",
    "digital_illustration_grain_20",
    "digital_illustration_graphic_intensity",
    "digital_illustration_hard_comics",
    "digital_illustration_long_shadow",
    "digital_illustration_modern_folk",
    "digital_illustration_multicolor",
    "digital_illustration_neon_calm",
    "digital_illustration_noir",
    "digital_illustration_nostalgic_pastel",
    "digital_illustration_outline_details",
    "digital_illustration_pastel_gradient",
    "digital_illustration_pastel_sketch",
    "digital_illustration_pop_art",
    "digital_illustration_pop_renaissance",
    "digital_illustration_quiet_curiosity",
    "digital_illustration_sketch_and_shade",
    "digital_illustration_street_art",
    "digital_illustration_tablet_sketch",
    "digital_illustration_urban_glow",
    "digital_illustration_urban_sketching",
    "digital_illustration_vanilla_dreams",
    "digital_illustration_young_adult_book",
    "digital_illustration_young_adult_book_2",
    # Vector Illustration Styles
    "vector_illustration",
    "vector_illustration_seamless",
    "vector_illustration_line_art",
    "vector_illustration_doodle_line_art",
    "vector_illustration_flat_2",
    "vector_illustration_70s",
    "vector_illustration_cartoon",
    "vector_illustration_kawaii",
    "vector_illustration_linocut",
    "vector_illustration_engraving",
    "vector_illustration_halloween_stickers",
    "vector_illustration_line_circuit",
    "vector_illustration_bold_stroke",
    "vector_illustration_chemistry",
    "vector_illustration_colored_stencil",
    "vector_illustration_contour_pop_art",
    "vector_illustration_cosmics",
    "vector_illustration_cutout",
    "vector_illustration_depressive",
    "vector_illustration_editorial",
    "vector_illustration_emotional_flat",
    "vector_illustration_infographical",
    "vector_illustration_marker_outline",
    "vector_illustration_mosaic",
    "vector_illustration_naivector",
    "vector_illustration_ornamenticute",
    "vector_illustration_roundish_flat",
    "vector_illustration_segmented_colors",
    "vector_illustration_sharp_contrast",
    "vector_illustration_thin",
    "vector_illustration_vector_photo",
    "vector_illustration_vivid_shapes",
]


def generate_image(
    prompt: str, style: str = "realistic_image", timeout: int = 30
) -> Optional[str]:
    """
    Generate an image using the Recraft API with a progress bar.

    Args:
        prompt (str): The image generation prompt
        style (str, optional): Style of the generated image. Defaults to "realistic_image".
        timeout (int, optional): Timeout for the API request. Defaults to 30 seconds.

    Returns:
        Optional[str]: Generated image URL or None if generation fails
    """
    # Validate style
    if style not in ALLOWED_STYLES:
        click.echo(
            f"\nError: Invalid style '{style}'. Allowed styles are: {', '.join(ALLOWED_STYLES)}"
        )
        return None

    api_token = ensure_token()

    url = "https://external.api.recraft.ai/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    data = {"prompt": prompt, "style": style}

    try:
        # Create a progress bar for image generation with continuous updates
        with tqdm(
            total=100, desc="Generating Image", bar_format="{l_bar}{bar}"
        ) as pbar:
            start_time = time.time()

            # Simulate continuous progress while waiting for the API
            def update_progress():
                elapsed = time.time() - start_time
                # Asymptotic progress that approaches 90% but never quite reaches it
                progress = min(90, 50 * (1 - math.exp(-0.2 * elapsed)))
                pbar.n = progress
                pbar.refresh()

            # Start a background thread for progress updates
            stop_event = threading.Event()

            def progress_thread():
                while not stop_event.is_set():
                    update_progress()
                    time.sleep(0.5)

            progress_updater = threading.Thread(target=progress_thread)
            progress_updater.start()

            try:
                # Make the actual API request
                response = httpx.post(url, headers=headers, json=data, timeout=timeout)
                response.raise_for_status()

                # Stop the progress thread
                stop_event.set()
                progress_updater.join()

                # Ensure progress bar reaches 100%
                pbar.n = 100
                pbar.refresh()

                return response.json()["data"][0]["url"]

            except Exception:
                # Stop the progress thread in case of any exception
                stop_event.set()
                progress_updater.join()
                raise

    except httpx.HTTPStatusError as exc:
        click.echo(
            f"\nHTTP error occurred: {exc.response.status_code} - {exc.response.text}"
        )
        return None
    except httpx.RequestError as exc:
        click.echo(f"\nRequest error occurred: {exc}")
        return None
    except Exception as exc:
        click.echo(f"\nUnexpected error occurred: {exc}")
        return None
