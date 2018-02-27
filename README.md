# good-morning
早安圖產生器

---
# Font

Download free font from:

https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/TraditionalChinese/SourceHanSansTC-Medium.otf

# Usage

    import goodmorning
    goodmorning.generate('爹娘早安！', font='SourceHanSansTC-Medium.otf', header_template=False)
    
This will return the path of the generated image:

    /tmp/shared/good-morning.jpg
    
Example image:

![](example.jpg)
