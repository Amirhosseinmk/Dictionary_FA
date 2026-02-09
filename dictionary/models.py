from django.db import models

class Word(models.Model):
    text = models.CharField(max_length=100, unique=True, verbose_name="کلمه")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['text']  # sort alphabetically by default
        verbose_name = "کلمه"
        verbose_name_plural = "کلمات"

    def __str__(self):
        return self.text

class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='definitions')
    text = models.TextField(verbose_name="معنی / تعریف")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="ترتیب")

    class Meta:
        ordering = ['order']
        verbose_name = "تعریف"
        verbose_name_plural = "تعاریف"

    def __str__(self):
        return f"{self.word} - تعریف {self.order}"