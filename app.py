# app.py
import streamlit as st
from utils.util import (
  upload_file_to_gemini,
  poll_file_processing,
  generate_transcription,
)
from utils.model import load_model

def main():
  st.set_page_config(page_title="تحليل مكالمات العملاء", layout="wide")
  
  # تحسين التصميم باستخدام Markdown وCSS
  st.markdown("""
      <style>
          body {
              direction: rtl;
              background-color: #FFFFFF;
          }
          .main-header {
              text-align: center;
              font-size: 2.5em;
              color: #007BFF; /* لون أزرق فاتح */
              margin-top: 20px;
              font-weight: bold;
          }
          .sub-header {
              text-align: center;
              font-size: 1.2em;
              color: #333333; /* لون رمادي غامق */
              margin-bottom: 30px;
          }
          .upload-section {
              text-align: center;
              margin-top: 20px;
          }
          .info-message {
              text-align: center;
              font-size: 1.1em;
              color: #555555; /* لون رمادي متوسط */
          }
          .description {
              text-align: center;
              font-size: 1em;
              color: #333333; /* لون رمادي غامق */
              margin-bottom: 20px;
          }
      </style>
  """, unsafe_allow_html=True)
  
  st.markdown("<div class='main-header'>تحليل مكالمات العملاء</div>", unsafe_allow_html=True)
  st.markdown("<div class='description'>اكتشف رؤى استراتيجية من مكالمات العملاء لتحسين أداء المبيعات.</div>", unsafe_allow_html=True)
  st.markdown("<div class='sub-header'>قم برفع ملف صوتي أو فيديو لتحليل مكالمة العميل واستخراج رؤى استراتيجية.</div>", unsafe_allow_html=True)

  model = load_model(type=None, schemaType=None)

  st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
  uploaded_file = st.file_uploader("اختر ملفًا صوتيًا أو فيديو", type=["mp3", "wav", "aiff", "acc", "ogg", "flac", "mp4", "avi", "mov"])
  st.markdown("</div>", unsafe_allow_html=True)

  if uploaded_file is not None:
      file_type = uploaded_file.type
      if file_type.startswith('audio'):
          st.audio(uploaded_file, format=file_type)
      elif file_type.startswith('video'):
          st.video(uploaded_file)
      
      if st.button("بدء التحليل"):
          with st.spinner('جاري رفع الملف...'):
              try:
                  uploaded_genai_file = upload_file_to_gemini(uploaded_file)
                  if uploaded_genai_file:
                      st.success("تم رفع الملف بنجاح!")
              except Exception as e:
                  st.error(f"حدث خطأ أثناء رفع الملف: {e}")
                  return

          processed_file = poll_file_processing(uploaded_genai_file)
          if processed_file is None:
              st.error("فشلت معالجة الملف.")
              return

          with st.spinner('جاري استخراج التحليل...'):
              transcription = generate_transcription(model, processed_file)
              if transcription:
                  st.success("تم التحليل بنجاح!")
                  st.markdown(transcription, unsafe_allow_html=True)
  else:
      st.markdown("<div class='info-message'>يرجى اختيار ملف صوتي أو فيديو للبدء في عملية التحليل.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
  main()