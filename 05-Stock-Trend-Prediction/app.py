import os, sys
import logging

from niftystocks import ns
from flask import Flask, render_template, request

from src.pipeline.pipeline import Pipeline
import shutil


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


app = Flask(__name__)


logger.info("Fetching the nifty_500 Stock Symbols")
nifty_500 = sorted(ns.get_nifty500_with_ns())
logger.info(f"Nifty 500 Stock Symbols are as follows : {nifty_500}")

def copy_files(file_list, destination_dir):
    logger.info("Copying Graphs Required from their respective paths to 'static/'")
    for source_file in file_list:
        try:
            shutil.copy(source_file, destination_dir)
            logger.info(f"File '{source_file}' copied successfully {destination_dir}")
        except Exception as e:
            logger.info(f"Error copying file '{source_file}': {e}")
            raise Exception(e, sys) from e
    logger.info("Completed copying the Graphs")
    

def start_pipeline(selected_stock):
    try:
        logger.info("Started Pipeline")
        pipeline = Pipeline()
        graph_1, graph_2, graph_3 = pipeline.run_pipeline(stock_symbol=selected_stock)
        logger.info(f"The graphs are at below paths\n{graph_1}\n{graph_2}\n{graph_3}")
        return graph_1, graph_2, graph_3
    except Exception as e:
        raise Exception(e, sys) from e


@app.route('/')
def index():
    try:
        logger.info("Rendering the Home Page")
        return render_template('index.html', stocks=nifty_500)
    except Exception as e:
        raise Exception(e, sys) from e

@app.route('/result', methods=['POST'])
def result():
    try:
        if request.method == 'POST':
            selected_stock = request.form['stocks']
            graph_1, graph_2, graph_3 = start_pipeline(selected_stock=selected_stock)
            file_list = [graph_1, graph_2, graph_3]
            destination_directory = 'static/'
            copy_files(file_list, destination_directory)
            logger.info(f"Selected stock : {selected_stock}")
            # Pass the paths of the graphs to the template
            logger.info("Rendering the Result Page")
            return render_template('result.html', stocks=nifty_500, graph_1=str(graph_1), graph_2=str(graph_2), graph_3=str(graph_3))
    except Exception as e:
        raise Exception(e, sys) from e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False)



