import flet as ft
import replicate
from bisect import bisect
from time import sleep

ADDITIONAL_PROMPT1=", ultra realistic in detail, vibrant, cinematic, dreamy, goals"
NEGATIVE_PROMPT1="BadDream, badhandv4, BadNegAnatomyV1-neg, easynegative, FastNegativeV2, bad anatomy, extra people, (deformed iris, deformed pupils, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation, signature, watermark, airbrush, photoshop, plastic doll, (ugly eyes, deformed iris, deformed pupils, fused lips and teeth:1.2), text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, masculine, obese, fat, out of frame, caricature, body horror, mutant, facebook, youtube, food, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
NEGATIVE_PROMPT2="ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, low resolution, 3d model, deformed hands, deformed feet, deformed face, deformed body parts, same haircut, eyes without pupils, doubled image, mid aged man, old men, logo in frame, gun, man with more than one penis on body, scared facial expression, drawing, painting, blur focus, blur, photo effects, skinny guy, make-up on male, angry facial expression, same human face in one frame, illustration, anime, cartoon, ugly face, bruises, cartoon, anime, painting, red color saturation, unattractive face, jpeg artifacts, frame, Violence, Gore, Blood, War, Weapons, Death, Destruction, Fire, Explosions, Pollution, Garbage, Graffiti, Vandalism, Rust, Decay, Filth, Disease, Insects, Rodents, Vermin, Darkness, Shadows, Nightmares, Fear, Horror, Sadness, Depression, Pain, Suffering, Anguish, Despair, Loneliness, Isolation, Neglect, Abandonment, Negativity, Hate, Racism, Sexism, Homophobia, Discrimination, Intolerance, Prejudice, Ignorance, Arrogance, Greed, Selfishness, Cruelty, Insanity, Madness, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, deformed, ugly, mutilated, disfigured, text, extra limbs, face cut, head cut, extra fingers, extra arms, poorly drawn face, mutation, bad proportions, cropped head, malformed limbs, mutated hands, fused fingers, long neck, illustration, painting, drawing, art, sketch, disfigured, kitsch, ugly, oversaturated, grain, low-res, Deformed, blurry, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, poorly drawn hands, missing limb, blurry, floating limbs, disconnected limbs, malformed hands, blur, out of focus, long neck, long body, ugly, disgusting, poorly drawn, childish, mutilated, , mangled, old, surreal"

models = [
    "lucataco/ssd-1b:1ee85ef681d5ad3d6870b9da1a4543cb3ad702d036fa5b5210f133b83b05a780",
    "luosiallen/latent-consistency-model:553803fd018b3cf875a8bc774c99da9b33f36647badfd88a6eec90d61c5f62fc",
    "lucataco/hotshot-xl:78b3a6257e16e4b241245d65c8b2b81ea2e1ff7ed4c55306b511509ddbfd327a",
]

watermark_base64 = "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"

def size_estimation(height,width):
    sizes = [384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024]
    h = sizes + [1024]
    return h[bisect(sizes, height)], h[bisect(sizes, width)]

def main(page: ft.Page):
    page.title = "AI VisionBoard"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0

    def prompt(e):
        print(dream_prompt.value)
        body.image_opacity=0.3
        page.update()
        height, width = size_estimation(page.height or page.window_height, page.width or page.window_width)
        selected_model = navigation_bar.selected_index or 0
        iterator = replicate.run(
            models[selected_model],
            input={"prompt": dream_prompt.value+ADDITIONAL_PROMPT1, "height":int(height), "width":int(width),
            "negative_prompt": NEGATIVE_PROMPT1}
        )

        if isinstance(iterator, str):
            iterator = [iterator]

        for image in iterator:
            body.image_src = image
            body.image_opacity=0.7
            print(dream_prompt.value, image)
            page.update()

        feedback_button_dislike.opacity=1
        feedback_button_like.opacity=1
        sleep(3)
        page.update()

    def navigation_bar_toggle(e):
        page.navigation_bar = None if page.navigation_bar else navigation_bar
        page.update()

    def settings_click(e):
        height = page.height or page.window_height
        width = page.width or page.window_width
        print(height,width)
        page.update()

    def prompt_focus(e):
        dream_prompt.opacity=1
        page.update()
        dream_prompt.focus()

    def prompt_blur(e):
        dream_prompt.opacity=0
        sleep(6)
        page.update()

    dream_prompt = ft.TextField( 
                    border="none", 
                    hint_text="Create your world...",
                    max_lines=3,
                    autofocus=True,
                    text_align=ft.TextAlign.CENTER,
                    on_submit=prompt,
                    on_focus=prompt_focus,
                    #on_blur=prompt_blur,
                    animate_opacity=999,
                    opacity=1,
                    )

    prompt_element = ft.Row([dream_prompt],alignment=ft.MainAxisAlignment.CENTER)

    top_buttons = ft.Row(
            [
                ft.IconButton(ft.icons.MENU_OUTLINED, on_click=navigation_bar_toggle),
                ft.IconButton(ft.icons.SETTINGS_OUTLINED, on_click=settings_click),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    
    def reset_feedback(like=True):
        page.update()
        feedback_button_dislike.opacity=0
        feedback_button_like.opacity=0
        if like:
            dream_prompt.opacity=0
            sleep(3)
        page.update()
        if like:
            dream_prompt.value=""
        else:
            dream_prompt.focus()


    def feedback_like(e):
        feedback_button_like.icon=ft.icons.THUMB_UP_ROUNDED
        reset_feedback(True)
        feedback_button_like.icon=ft.icons.THUMB_UP_OUTLINED
        

    def feedback_dislike(e):
        feedback_button_dislike.icon=ft.icons.THUMB_DOWN_ROUNDED
        reset_feedback(False)
        feedback_button_dislike.icon=ft.icons.THUMB_DOWN_OUTLINED
        

    feedback_button_dislike=ft.IconButton(ft.icons.THUMB_DOWN_OUTLINED,animate_opacity=999,on_click=feedback_dislike)
    feedback_button_dislike.opacity=0
    feedback_button_like=ft.IconButton(ft.icons.THUMB_UP_OUTLINED,animate_opacity=999,on_click=feedback_like)
    feedback_button_like.opacity=0
    watermark_image=ft.Image(src="assets/images/watermark2.png",fit=ft.ImageFit.SCALE_DOWN,height=33)
    watermark_image.opacity=0.9
    bottom_buttons = ft.Row(
            [
                feedback_button_dislike,
                watermark_image,
                feedback_button_like,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
           
    body = ft.Container(
        ft.SafeArea(ft.Column([top_buttons, prompt_element, bottom_buttons], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
        image_src="assets/images/aivision1.jpg",
        image_fit=ft.ImageFit.COVER,
        image_opacity=0.3,
        expand=True,
        height=13371337,
        animate_opacity=3333,
        opacity=0.9,
        on_click=prompt_focus,
        )

    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.IMAGE_OUTLINED, label="Current"),
            ft.NavigationDestination(icon=ft.icons.IMAGE_ROUNDED, label="Test"),
            ft.NavigationDestination(icon=ft.icons.VIDEO_LIBRARY_OUTLINED, label="Video"),
        ],
        on_change=navigation_bar_toggle,
    )

    page.add(body)

ft.app(
    target=main,
    assets_dir="assets"
)
