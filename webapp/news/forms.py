from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user


class CommentForm(FlaskForm):
    news_id = HiddenField(
        'ID новости',
        validators=[DataRequired()])

    text = StringField(
        'Текст комментария',
        validators=[DataRequired()],
        render_kw={"class": "form-control"})

    submit = SubmitField(
        'Отправить!',
        render_kw={"class": "btn btn-primary"})

    def validate_text(self, text):
        if current_user.is_anonymous:
            raise ValidationError(
                'Зарегистируйтесь, чтобы оставить комментарий')
