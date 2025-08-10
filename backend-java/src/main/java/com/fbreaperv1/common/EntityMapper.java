package com.fbreaperv1.common;

import com.fbreaperv1.dto.PostDTO;
import com.fbreaperv1.model.Post;
import com.fbreaperv1.dto.CommentDTO;
import com.fbreaperv1.model.Comment;
import org.springframework.stereotype.Component;

@Component
public class EntityMapper {
    public PostDTO toPostDTO(Post post) {
        return new PostDTO(
            post.getId() != null ? post.getId().toString() : null,
            post.getContent(),
            post.getCreatedTime(),
            post.getAuthor(),
            post.getPostType(),
            null,
            post.getHashtags() != null ? String.join(",", post.getHashtags()) : null
        );
    }
    public CommentDTO toCommentDTO(Comment comment) {
        return new CommentDTO(
            comment.getId() != null ? comment.getId().toString() : null,
            comment.getContent(),
            comment.getCreatedTime(),
            comment.getAuthor(),
            null,
            null
        );
    }
}
