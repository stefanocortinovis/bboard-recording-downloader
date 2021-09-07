from .parser import parser
from .scraper import get_driver, get_video_src, download_video
from .utils import validate


def main():
    args = parser.parse_args()
    validated_args = validate(args)

    driver = get_driver(validated_args['browser'], validated_args['executable_path'], validated_args['headless'])
    recording_title, recording_date, video_src = get_video_src(driver, validated_args['url'], validated_args['T'])
    download_video(video_src, validated_args['dest'], recording_date, recording_title, validated_args['course'])

if __name__ == '__main__':
    main()
