# good-morning
早安圖產生器

---
# Font

Download free font from:

https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/TraditionalChinese/SourceHanSansTC-Medium.otf

# Usage

    from goodmorning.image import generate
    generate('爹，娘， ', font_path='/your/font/path/SourceHanSansTC-Medium.otf')
    
This will return the path of the generated image:

    /tmp/shared/good-morning.jpg
    
Example image:

![](example.jpg)
