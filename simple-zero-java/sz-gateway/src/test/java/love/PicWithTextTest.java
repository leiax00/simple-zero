package love;

import org.junit.Test;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileOutputStream;

/**
 * 将正常图片转换成用文字书写的图片
 */
public class PicWithTextTest {
    @Test
    public void writePic() {
        String base = "lxl";
        String picPath = "./src/test/resources/love/pic.jpg";
        try {
            BufferedImage image = ImageIO.read(new File(picPath));
            BufferedImage newImage = new BufferedImage(image.getWidth(), image.getHeight(), image.getType());
            Graphics2D graphics2D = (Graphics2D) newImage.getGraphics();
            graphics2D.setFont(new Font("Consolas", Font.PLAIN, 12));
            int index = 0;
            for (int y = 0; y < image.getHeight(); y += 12) {
                for (int x = 0; x < image.getWidth(); x += 12) {
                    int pxColor = image.getRGB(x, y);
                    int r = (pxColor & 0xff0000) >> 16,
                            g = (pxColor & 0xff00) >> 8,
                            b = pxColor & 0xff;
                    graphics2D.setColor(new Color(r, g, b));
                    graphics2D.drawString(String.valueOf(base.charAt(index % base.length())), x, y);
                    index++;
                }
            }
            ImageIO.write(newImage, "JPG", new FileOutputStream("./src/test/java/love/temp.jpg"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
