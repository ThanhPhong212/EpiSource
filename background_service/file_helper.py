from reportlab.pdfgen import canvas

def create_pdf(post, filename):
    c = canvas.Canvas(filename)
    c.drawString(50, 800, "Thông tin Post")
    c.drawString(50, 780, f"Title: {post.Title}")
    c.drawString(50, 760, f"Description: {post.Description}")
    c.drawString(50, 740, f"Price: {post.Price}")
    c.save()
