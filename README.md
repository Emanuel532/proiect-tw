# SkillTrade

## 1 for sample data creation

```$python manage.py create_sample_data```

## routes for get requests

 + <strong>root</strong> -> app landing page
 + <strong>admin/</strong> -> admin panel
 + <strong>posts/</strong> -> lists all posts
 + <strong>posts/post_id={your_post_id}/</strong> -> view a certain post based on it's id
 + <strong>author/user_id={your_user_id}/posts/</strong> -> view all the posts of a certain user by it's id
 + <strong>author/user_id={your_user_id}/post_id={your_post_id}/</strong> -> view x user's y post
 + <strong>skills/skill_id={your_skill_id}/offered/</strong> -> view all posts that offer a certain skill
 + <strong>skills/skill_id={your_skill_id}/needed/</strong> -> view all posts that need a certain skill
 + <strong>account/</strong>
 + <strong>accounts/</strong>
