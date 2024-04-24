#add Bash alias/function to quickly display colorized banners:
#https://blog.victormendonca.com/2019/03/10/colorful-banners-with-figlet-and-lolcat/
lolbanner ()
{
    echo
    figlet -f ~/.local/share/fonts/3d.flf $* | lolcat
    echo
}
