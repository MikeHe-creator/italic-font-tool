from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

def italicize_glyph(glyph, italic_angle, glyf_table):
    if glyph.isComposite():
        for component in glyph.components:
            base_glyph = glyf_table[component.glyphName]
            italicized_base_glyph = italicize_glyph(base_glyph, italic_angle, glyf_table)
            glyf_table[component.glyphName] = italicized_base_glyph
        return glyph

    new_pen = TTGlyphPen(glyf_table)
    transform = (1, 0, italic_angle, 1, 0, 0)
    pen = TransformPen(new_pen, transform)

    glyph.draw(pen, glyf_table)

    return new_pen.glyph()


def italicize_font(font_path, italic_angle, output_path):
    font = TTFont(font_path)
    glyf_table = font['glyf']

    for glyph_name in font.getGlyphOrder():
        glyph = glyf_table[glyph_name]
        if not glyph.isComposite():
            italicized_glyph = italicize_glyph(glyph, italic_angle, glyf_table)
            glyf_table[glyph_name] = italicized_glyph
    if 'post' in font:
        font['post'].italicAngle = italic_angle * 180 / 3.14159
    font.save(output_path)

italic_angle = 0.3
input_font_path = "E:/document file/JavaScript/vuep01/MikeReader/pages/Elements/font/Misans/MiSans-Normal.ttf"
output_font_path = "E:/document file/JavaScript/vuep01/MikeReader/pages/Elements/font/Misans/MiSans-Italic.ttf"

italicize_font(input_font_path, italic_angle, output_font_path)
