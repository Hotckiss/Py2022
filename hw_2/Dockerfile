FROM python:3.9
RUN apt-get update
RUN apt-get install -y texlive-latex-base  && apt-get install -y graphviz

WORKDIR app

RUN python3.9 -m pip install hotckissast==1.0.1
COPY src/ .

CMD python3.9 latex_generator.py && pdflatex -output-directory ../artifacts ../artifacts/table.tex && rm ../artifacts/table.log ../artifacts/table.aux