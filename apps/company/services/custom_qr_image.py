from PIL import Image, ImageFont, ImageDraw, ImageOps
from .generate_qr_code import qrcode_generator


def create_qr_titles(title1, title2, title3, domain):
    """ creating custom image with qr and titles """
    theme_color = '#A770EF'
    # Scale up 4x for text, scale down with antialias, and then add qrcode
    multiplier = 4
    width = 2 * 250 * multiplier
    height = 2 * 250 * multiplier

    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Generate QR, titles before placing so that widths and heights can
    # be used to calculate placement
    # Generate QR Code
    qr_img = qrcode_generator(domain)
    qr_img_w, qr_img_h = qr_img.size

    font_size = 50 * multiplier
    font_style = ImageFont.truetype(
        'static/fonts/montserrat-bold.ttf', (font_size + 30)
    )
    font_domen_style = ImageFont.truetype(
        'static/fonts/montserrat-regular.ttf', font_size
    )

    # Generate title1
    title1_w, title1_h = draw.textsize(text=title1, font=font_style)
    # Generate title2
    title2_w, title2_h = draw.textsize(text=title2, font=font_style)
    # Generate title3
    title3_w, title3_h = draw.textsize(text=title3, font=font_style)
    # Generate domain title (title4)
    domain_w, domain_h = draw.textsize(text=domain, font=font_domen_style)

    # Place title1
    draw.text(xy=(((width - title1_w) / 2), round(height / qr_img_h) + 80),
              text=title1, font=font_style, fill='black')
    # Place domain title
    draw.text(xy=(((width - domain_w) / 2), round(height - qr_img_h) - 100),
              text=domain, font=font_domen_style, fill=theme_color)

    # create images for transparent bg and rotate titles
    # left side title
    image_rgba_left_side = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw1 = ImageDraw.Draw(image_rgba_left_side)
    draw1.text((round((width - title2_w) / 2), round(height / qr_img_h)),
               text=title2, font=font_style, fill='black')
    # right side title
    image_rgba_right_side = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(image_rgba_right_side)
    draw2.text((round((width - title3_w) / 2), round(height / qr_img_h)),
               text=title3, font=font_style, fill='black')

    # Place side titles
    image.paste(image_rgba_left_side, box=(80, 0),
                mask=image_rgba_left_side.rotate(90))
    image.paste(image_rgba_right_side, box=(-80, 0),
                mask=image_rgba_right_side.rotate(-90))

    # add color border
    image = ImageOps.expand(image, border=50, fill=theme_color)

    # Resize (for text anti-aliasing purposes)
    image = image.resize((int(width / multiplier), int(height / multiplier)))

    # Place QR code
    image.paste(
        qr_img,
        box=(
            round((int(width / multiplier) - qr_img_w) / 2),
            round((int(height / multiplier) - qr_img_h) / 2)
        )
    )
    return image
