#!/usr/bin/env python3

#   Copyright 2023 James Andariese
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json

import requests

from flask import Flask, request, jsonify

import yt_dlp

app = Flask(__name__)

@app.route('/health', methods = ['GET'])
def health():
    return 'ok'

@app.route('/<vid>', methods = ['GET'])
def success(vid):
    ydl = yt_dlp.YoutubeDL({})
    info = ydl.extract_info("https://www.youtube.com/watch?v="+vid, download=False)
    words = []

    # get the most automated (probably accurate rather than possibly self-censored)
    cap = (
        [c for c in info.get('automatic_captions', {}).get('en', []) if c['ext'] == 'json3']
        + [c for c in info.get('subtitles', {}).get('en', []) if c['ext'] == 'json3']
    )

    # if neither automatic_captions or subtitles had english versions, len(cap) will be 0
    if len(cap) > 0:
        cap = cap[0]
        resp = requests.get(cap['url'])
    
        for e in json.loads(resp.content)['events']:
            for seg in e.get('segs', []):
                txt = seg['utf8']
                txt.replace('\\n', '\n')
                words.append(txt)
    
    return {
        "title": info['title'],
        "text": ' '.join(words),
        "description": info['description']
    }


if __name__ == '__main__':
    import os
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=8000, debug=False)

